"""Property-style tests for audit chain integrity."""

from __future__ import annotations

import hashlib
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from workbench.audit import AuditStore, compute_chain_hash, verify_audit_chain

pytestmark = pytest.mark.phase0


@given(
    prev_hash=st.text(
        min_size=64,
        max_size=64,
        alphabet=st.characters(min_codepoint=48, max_codepoint=102),
    ),
    payload_text=st.text(min_size=1, max_size=200),
)
def test_chain_hash_recomputation_is_stable(prev_hash: str, payload_text: str) -> None:
    payload_hash = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
    kwargs = {
        "prev_hash": prev_hash,
        "payload_hash": payload_hash,
        "event_id": "evt-1",
        "event_type": "bias_battery.result",
        "timestamp_utc": "2026-07-22T00:00:00+00:00",
        "model_id": "model",
        "model_version": "v1",
        "materiality_tier": "T3",
        "actor": "validator@example.com",
        "finos_control": "mi-5",
        "finos_tier": 2,
    }
    first = compute_chain_hash(**kwargs)
    second = compute_chain_hash(**kwargs)
    assert first == second


def test_tampered_payload_breaks_verify_chain(tmp_path: Path) -> None:
    db_path = tmp_path / "tamper.db"
    store = AuditStore(db_path)
    store.append_event(
        event_id=str(uuid.uuid4()),
        event_type="bias_battery.result",
        timestamp_utc=datetime.now(UTC).isoformat(),
        model_id="m",
        model_version="v",
        materiality_tier="T3",
        actor="validator@example.com",
        payload={"reasoning": {"summary": "ok"}, "value": 1},
        finos_control="mi-5",
        finos_tier=2,
    )

    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET payload_json = ? WHERE seq_id = 1", ('{"value":2}',))

    verification = verify_audit_chain(db_path)
    assert verification.status == "FAIL"
    assert any("payload_hash mismatch" in issue for issue in verification.breaks)


def test_seq_id_is_monotonic(tmp_path: Path) -> None:
    db_path = tmp_path / "seq.db"
    store = AuditStore(db_path)
    for index in range(6):
        store.append_event(
            event_id=str(uuid.uuid4()),
            event_type="validation_run.start",
            timestamp_utc=datetime.now(UTC).isoformat(),
            model_id="m",
            model_version="v",
            materiality_tier="T3",
            actor="validator@example.com",
            payload={"reasoning": {"summary": "ok"}, "idx": index},
            finos_control="mi-5",
            finos_tier=2,
        )

    events = store.events()
    seq_ids = [int(row["seq_id"]) for row in events]
    assert seq_ids == list(range(1, len(seq_ids) + 1))
