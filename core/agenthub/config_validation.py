from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    return json.loads(Path(schema_path).read_text(encoding="utf-8"))


def validate_workbench_config(config_path: str | Path, schema_path: str | Path) -> dict[str, Any]:
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    schema = load_schema(schema_path)
    jsonschema.validate(instance=config, schema=schema)
    return config
