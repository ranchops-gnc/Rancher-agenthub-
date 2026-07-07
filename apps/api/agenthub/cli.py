from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

DEFAULT_HOME = Path.home() / ".agenthub"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def command_doctor(args: argparse.Namespace) -> None:
    home = Path(args.home).expanduser()
    required = ["AGENTS.md", "skills", "agents", "memory", "profile"]
    missing = [item for item in required if not (home / item).exists()]
    if missing:
        print(json.dumps({"status": "warning", "home": str(home), "missing": missing}, indent=2))
        return
    print(json.dumps({"status": "ok", "home": str(home)}, indent=2))


def command_validate(args: argparse.Namespace) -> None:
    config_path = Path(args.config).expanduser()
    schema_path = Path(args.schema).expanduser()
    config = load_yaml(config_path)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(config), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "<root>"
            print(f"{path}: {error.message}")
        raise SystemExit(1)
    print(json.dumps({"status": "valid", "config": str(config_path)}, indent=2))


def command_skill_list(args: argparse.Namespace) -> None:
    skills_dir = Path(args.home).expanduser() / "skills"
    skills = sorted(path.name for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.exists() else []
    print(json.dumps({"skills": skills}, indent=2))


def command_agent_list(args: argparse.Namespace) -> None:
    agents_dir = Path(args.home).expanduser() / "agents"
    agents = sorted(path.name for path in agents_dir.iterdir() if path.is_file()) if agents_dir.exists() else []
    print(json.dumps({"agents": agents}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agenthub", description="AgentHub command-line interface")
    parser.add_argument("--home", default=str(DEFAULT_HOME), help="AgentHub home directory")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check local AgentHub installation")
    doctor.set_defaults(func=command_doctor)

    validate = sub.add_parser("validate", help="Validate a workbench YAML config")
    validate.add_argument("config")
    validate.add_argument("--schema", default="config/agent-workbench.schema.json")
    validate.set_defaults(func=command_validate)

    skill = sub.add_parser("skill", help="Skill commands")
    skill_sub = skill.add_subparsers(dest="skill_command", required=True)
    skill_list = skill_sub.add_parser("list", help="List local skills")
    skill_list.set_defaults(func=command_skill_list)

    agent = sub.add_parser("agent", help="Agent commands")
    agent_sub = agent.add_subparsers(dest="agent_command", required=True)
    agent_list = agent_sub.add_parser("list", help="List local agent files")
    agent_list.set_defaults(func=command_agent_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
