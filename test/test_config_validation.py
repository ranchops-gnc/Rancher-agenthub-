from pathlib import Path

import pytest

from agenthub.config_validation import validate_workbench_config


def test_validate_example_workbench_config() -> None:
    root = Path(__file__).resolve().parents[1]
    config = validate_workbench_config(
        root / "config" / "agent-workbench.example.yaml",
        root / "config" / "agent-workbench.schema.json",
    )
    assert "agents" in config
    assert "workflows" in config


def test_invalid_config_rejected(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("agents: {}\n", encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    with pytest.raises(Exception):
        validate_workbench_config(invalid, root / "config" / "agent-workbench.schema.json")
