#!/usr/bin/env bash
set -euo pipefail

AGENTHUB_HOME="${AGENTHUB_HOME:-$HOME/.agenthub}"
REPO_URL="${AGENTHUB_REPO_URL:-https://github.com/ranchops-gnc/Rancher-agenthub-.git}"

print_menu() {
  cat <<'MENU'
AgentHub Installer

1) Install AgentHub
2) Update AgentHub
3) Reinstall AgentHub
4) Uninstall AgentHub
5) Open configuration directory
6) Exit
MENU
}

install_agenthub() {
  if [ -d "$AGENTHUB_HOME/.git" ]; then
    echo "AgentHub is already installed at $AGENTHUB_HOME"
    exit 0
  fi

  command -v git >/dev/null 2>&1 || { echo "git is required"; exit 1; }
  mkdir -p "$(dirname "$AGENTHUB_HOME")"
  git clone "$REPO_URL" "$AGENTHUB_HOME"
  mkdir -p "$AGENTHUB_HOME/secrets" "$AGENTHUB_HOME/memory/session" "$AGENTHUB_HOME/memory/persist"
  chmod 700 "$AGENTHUB_HOME/secrets"
  echo "AgentHub installed at $AGENTHUB_HOME"
}

update_agenthub() {
  if [ ! -d "$AGENTHUB_HOME/.git" ]; then
    echo "AgentHub is not installed at $AGENTHUB_HOME"
    exit 1
  fi
  git -C "$AGENTHUB_HOME" pull --ff-only
  echo "AgentHub updated"
}

reinstall_agenthub() {
  rm -rf "$AGENTHUB_HOME"
  install_agenthub
}

uninstall_agenthub() {
  rm -rf "$AGENTHUB_HOME"
  echo "AgentHub removed from $AGENTHUB_HOME"
}

open_config_dir() {
  mkdir -p "$AGENTHUB_HOME"
  if command -v open >/dev/null 2>&1; then
    open "$AGENTHUB_HOME"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$AGENTHUB_HOME"
  else
    echo "$AGENTHUB_HOME"
  fi
}

main() {
  print_menu
  read -r -p "Choose an option: " choice
  case "$choice" in
    1) install_agenthub ;;
    2) update_agenthub ;;
    3) reinstall_agenthub ;;
    4) uninstall_agenthub ;;
    5) open_config_dir ;;
    6) exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
}

main "$@"
