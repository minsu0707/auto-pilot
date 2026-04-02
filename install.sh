#!/usr/bin/env bash

set -euo pipefail

REPO_SLUG="${AUTO_PILOT_REPO_SLUG:-minsu0707/auto-pilot}"
REPO_REF="${AUTO_PILOT_REPO_REF:-main}"
SCRIPT_URL="https://raw.githubusercontent.com/${REPO_SLUG}/${REPO_REF}/auto-pilot/install.sh"
SCRIPT_SOURCE="${BASH_SOURCE[0]:-}"

if [[ -n "${SCRIPT_SOURCE}" && "${SCRIPT_SOURCE}" != "bash" && "${SCRIPT_SOURCE}" != "-" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${SCRIPT_SOURCE}")" && pwd)"
  LOCAL_SCRIPT="${SCRIPT_DIR}/auto-pilot/install.sh"
  if [[ -f "${LOCAL_SCRIPT}" ]]; then
    exec bash "${LOCAL_SCRIPT}"
  fi
fi

curl -fsSL "${SCRIPT_URL}" | bash
