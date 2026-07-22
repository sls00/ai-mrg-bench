"""Workbench CLI entry point (P0+ implementation)."""

from __future__ import annotations

import typer

app = typer.Typer(
    name="workbench",
    help="Model risk validation, audit chain verification, and OCC reporting.",
    no_args_is_help=True,
)


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


if __name__ == "__main__":
    main()
