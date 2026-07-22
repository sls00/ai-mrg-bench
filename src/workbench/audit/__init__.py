"""Append-only hash-chained audit log utilities."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

GENESIS_PREV_HASH = "0" * 64
TIER2_EVENT_TYPES = {
    "bias_battery.result",
    "adverse_action.attribution",
    "adverse_action.methodology_published",
}


@dataclass(slots=True)
class AuditVerification:
    status: str
    total_events: int
    event_type_counts: dict[str, int]
    breaks: list[str]


class AuditStore:
    """SQLite-backed audit log with hash chaining."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def append_event(
        self,
        *,
        event_id: str,
        event_type: str,
        timestamp_utc: str,
        model_id: str,
        model_version: str,
        materiality_tier: str,
        actor: str,
        payload: dict[str, Any],
        finos_control: str,
        finos_tier: int,
        artifact_refs: list[dict[str, str]] | None = None,
    ) -> int:
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        prev_hash = self._last_payload_hash()
        metadata = _chain_metadata(
            event_id=event_id,
            event_type=event_type,
            timestamp_utc=timestamp_utc,
            model_id=model_id,
            model_version=model_version,
            materiality_tier=materiality_tier,
            actor=actor,
            finos_control=finos_control,
            finos_tier=finos_tier,
        )
        chain_hash = hashlib.sha256(f"{prev_hash}{payload_hash}{metadata}".encode()).hexdigest()
        artifact_refs_json = None
        if artifact_refs:
            artifact_refs_json = json.dumps(artifact_refs, sort_keys=True, separators=(",", ":"))

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO audit_log (
                    event_id, event_type, timestamp_utc, model_id, model_version,
                    materiality_tier, actor, payload_json, payload_hash, prev_hash,
                    chain_hash, finos_control, finos_tier, artifact_refs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    event_type,
                    timestamp_utc,
                    model_id,
                    model_version,
                    materiality_tier,
                    actor,
                    payload_json,
                    payload_hash,
                    prev_hash,
                    chain_hash,
                    finos_control,
                    finos_tier,
                    artifact_refs_json,
                ),
            )
            if cursor.lastrowid is None:
                raise RuntimeError("Failed to retrieve inserted audit seq_id.")
            return int(cursor.lastrowid)

    def events(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM audit_log ORDER BY seq_id ASC").fetchall()
        return [dict(row) for row in rows]

    def _last_payload_hash(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT payload_hash FROM audit_log ORDER BY seq_id DESC LIMIT 1"
            row = conn.execute(query).fetchone()
        if row is None:
            return GENESIS_PREV_HASH
        return str(row[0])

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_log (
                    seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    event_type TEXT NOT NULL,
                    timestamp_utc TEXT NOT NULL,
                    model_id TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    materiality_tier TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_hash TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    chain_hash TEXT NOT NULL,
                    finos_control TEXT NOT NULL,
                    finos_tier INTEGER NOT NULL,
                    artifact_refs TEXT
                )
                """,
            )
            conn.execute(
                """
                CREATE TRIGGER IF NOT EXISTS audit_log_no_update
                BEFORE UPDATE ON audit_log
                BEGIN
                    SELECT RAISE(ABORT, 'audit_log is append-only');
                END;
                """,
            )
            conn.execute(
                """
                CREATE TRIGGER IF NOT EXISTS audit_log_no_delete
                BEFORE DELETE ON audit_log
                BEGIN
                    SELECT RAISE(ABORT, 'audit_log is append-only');
                END;
                """,
            )


def compute_chain_hash(
    *,
    prev_hash: str,
    payload_hash: str,
    event_id: str,
    event_type: str,
    timestamp_utc: str,
    model_id: str,
    model_version: str,
    materiality_tier: str,
    actor: str,
    finos_control: str,
    finos_tier: int,
) -> str:
    metadata = _chain_metadata(
        event_id=event_id,
        event_type=event_type,
        timestamp_utc=timestamp_utc,
        model_id=model_id,
        model_version=model_version,
        materiality_tier=materiality_tier,
        actor=actor,
        finos_control=finos_control,
        finos_tier=finos_tier,
    )
    return hashlib.sha256(f"{prev_hash}{payload_hash}{metadata}".encode()).hexdigest()


def verify_audit_chain(db_path: Path) -> AuditVerification:
    store = AuditStore(db_path)
    rows = store.events()
    breaks: list[str] = []
    event_counts: dict[str, int] = {}
    expected_seq = 1
    previous_payload_hash = GENESIS_PREV_HASH

    for row in rows:
        event_counts[row["event_type"]] = event_counts.get(row["event_type"], 0) + 1
        if int(row["seq_id"]) != expected_seq:
            breaks.append(
                f"seq_id monotonicity break at {row['seq_id']} (expected {expected_seq})",
            )
            expected_seq = int(row["seq_id"])
        expected_seq += 1

        payload_hash = hashlib.sha256(str(row["payload_json"]).encode()).hexdigest()
        if payload_hash != row["payload_hash"]:
            breaks.append(f"payload_hash mismatch at seq_id={row['seq_id']}")
        if row["prev_hash"] != previous_payload_hash:
            breaks.append(f"prev_hash mismatch at seq_id={row['seq_id']}")

        expected_chain = compute_chain_hash(
            prev_hash=row["prev_hash"],
            payload_hash=row["payload_hash"],
            event_id=row["event_id"],
            event_type=row["event_type"],
            timestamp_utc=row["timestamp_utc"],
            model_id=row["model_id"],
            model_version=row["model_version"],
            materiality_tier=row["materiality_tier"],
            actor=row["actor"],
            finos_control=row["finos_control"],
            finos_tier=int(row["finos_tier"]),
        )
        if expected_chain != row["chain_hash"]:
            breaks.append(f"chain_hash mismatch at seq_id={row['seq_id']}")

        if row["event_type"] in TIER2_EVENT_TYPES and int(row["finos_tier"]) >= 2:
            payload = json.loads(str(row["payload_json"]))
            if "reasoning" not in payload:
                breaks.append(f"tier2 reasoning payload missing at seq_id={row['seq_id']}")

        previous_payload_hash = row["payload_hash"]

    status = "PASS" if not breaks else "FAIL"
    return AuditVerification(
        status=status,
        total_events=len(rows),
        event_type_counts=event_counts,
        breaks=breaks,
    )


def _chain_metadata(
    *,
    event_id: str,
    event_type: str,
    timestamp_utc: str,
    model_id: str,
    model_version: str,
    materiality_tier: str,
    actor: str,
    finos_control: str,
    finos_tier: int,
) -> str:
    metadata = {
        "actor": actor,
        "event_id": event_id,
        "event_type": event_type,
        "finos_control": finos_control,
        "finos_tier": finos_tier,
        "materiality_tier": materiality_tier,
        "model_id": model_id,
        "model_version": model_version,
        "timestamp_utc": timestamp_utc,
    }
    return json.dumps(metadata, sort_keys=True, separators=(",", ":"))
