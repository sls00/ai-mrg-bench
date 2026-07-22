"""FastAPI thin-app tests for the P2 endpoints (POST /validate, GET /report/{run_id},
GET /audit/verify). Endpoints are direct passthroughs to ValidationRun /
verify_audit_chain; these tests exercise the HTTP contract, not the SDK logic
(already covered by tests/phase0-2).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from workbench.api import app

pytestmark = [pytest.mark.phase2, pytest.mark.api]


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def isolated_config(tmp_path: Path) -> Path:
    """A P0 config (fast: no adverse_action/drift) rewritten to isolated tmp paths."""
    payload = yaml.safe_load(Path("configs/german_credit_p0.yaml").read_text())
    payload["validation_run"]["run_id"] = "api-test-run"
    payload["validation_run"]["audit"]["db_path"] = str(tmp_path / "workbench.db")
    payload["validation_run"]["outputs"]["artifact_dir"] = str(tmp_path / "{run_id}")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(payload))
    return config_path


def test_post_validate_runs_and_returns_summary(
    client: TestClient, isolated_config: Path,
) -> None:
    response = client.post("/validate", json={"config": str(isolated_config)})
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "api-test-run"
    assert body["status"] == "PASS"
    assert Path(body["report_path"]).exists()
    assert Path(body["artifact_dir"]).is_dir()


def test_get_report_returns_markdown(
    client: TestClient, isolated_config: Path, tmp_path: Path,
) -> None:
    client.post("/validate", json={"config": str(isolated_config)})
    response = client.get(
        "/report/api-test-run",
        params={"artifacts_root": str(tmp_path)},
    )
    assert response.status_code == 200
    assert "## I. Introduction" in response.text
    assert "text/plain" in response.headers["content-type"]


def test_get_audit_verify_returns_status(
    client: TestClient, isolated_config: Path, tmp_path: Path,
) -> None:
    client.post("/validate", json={"config": str(isolated_config)})
    db_path = tmp_path / "workbench.db"
    response = client.get("/audit/verify", params={"db": str(db_path)})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "PASS"
    assert body["events"] >= 4
    assert body["breaks"] == []


def test_post_validate_missing_config_returns_400(
    client: TestClient, tmp_path: Path,
) -> None:
    response = client.post("/validate", json={"config": str(tmp_path / "does-not-exist.yaml")})
    assert response.status_code == 400


def test_get_report_unknown_run_id_returns_404(
    client: TestClient, tmp_path: Path,
) -> None:
    response = client.get(
        "/report/no-such-run",
        params={"artifacts_root": str(tmp_path)},
    )
    assert response.status_code == 404


def test_get_audit_verify_missing_db_returns_404(
    client: TestClient, tmp_path: Path,
) -> None:
    response = client.get("/audit/verify", params={"db": str(tmp_path / "missing.db")})
    assert response.status_code == 404
