from __future__ import annotations

from pathlib import Path

import click
import uvicorn

from agenthub.config_validation import validate_workbench_config


@click.group()
def main() -> None:
    """AgentHub CLI."""


@main.command("serve")
@click.option("--host", default="0.0.0.0", show_default=True)
@click.option("--port", default=8000, show_default=True, type=int)
def serve(host: str, port: int) -> None:
    uvicorn.run("agenthub.main:app", host=host, port=port, reload=False)


@main.command("validate-config")
@click.argument("config_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--schema-path",
    default=Path("config/agent-workbench.schema.json"),
    show_default=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def validate_config(config_path: Path, schema_path: Path) -> None:
    validate_workbench_config(config_path, schema_path)
    click.echo("Configuration is valid.")
