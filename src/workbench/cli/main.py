"""Workbench CLI entry point."""

from __future__ import annotations

from pathlib import Path

import typer

from workbench.audit import verify_audit_chain
from workbench.sdk import ValidationRun

app = typer.Typer(
    name="workbench",
    help="Model risk validation, audit chain verification, and OCC reporting.",
    no_args_is_help=True,
)
validate_app = typer.Typer(name="validate", help="Validation workflows.")
audit_app = typer.Typer(name="audit", help="Audit log workflows.")
CONFIG_OPTION = typer.Option(..., "--config", exists=True, file_okay=True)
DB_OPTION = typer.Option(Path("workbench.db"), "--db")


@app.callback()
def main_callback() -> None:
    """Workbench CLI root (P0+ adds validate, audit, report)."""


@app.command("version")
def show_version() -> None:
    """Print package version."""
    from workbench import __version__

    typer.echo(__version__)


def main() -> None:
    app()


@validate_app.command("run")
def validate_run(config: Path = CONFIG_OPTION) -> None:
    """Run one validation workflow from a YAML config."""
    run = ValidationRun.from_config(config)
    result = run.run()
    typer.echo(f"run_id={result.run_id}")
    typer.echo(f"artifact_dir={result.artifact_dir}")
    typer.echo(f"report_path={result.report_path}")
    typer.echo("status=PASS")


@audit_app.command("verify-chain")
def audit_verify_chain(db: Path = DB_OPTION) -> None:
    """Verify audit hash-chain integrity."""
    verification = verify_audit_chain(db)
    typer.echo(f"status={verification.status}")
    typer.echo(f"events={verification.total_events}")
    typer.echo(f"breaks={len(verification.breaks)}")
    for event_type, count in sorted(verification.event_type_counts.items()):
        typer.echo(f"{event_type}={count}")
    if verification.status != "PASS":
        raise typer.Exit(code=1)


app.add_typer(validate_app)
app.add_typer(audit_app)


if __name__ == "__main__":
    main()
