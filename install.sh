#!/usr/bin/env bash

set -euo pipefail

REPO_SLUG="${AUTO_PILOT_REPO_SLUG:-minsu0707/auto-pilot}"
REPO_REF="${AUTO_PILOT_REPO_REF:-main}"
INSTALL_DIR="${AUTO_PILOT_INSTALL_DIR:-$HOME/plugins/auto-pilot}"
MARKETPLACE_PATH="${AUTO_PILOT_MARKETPLACE_PATH:-$HOME/.agents/plugins/marketplace.json}"
MARKETPLACE_SOURCE_PATH="${AUTO_PILOT_SOURCE_PATH:-./plugins/auto-pilot}"
TMP_ROOT="${TMPDIR:-/tmp}"
WORK_DIR="$(mktemp -d "${TMP_ROOT%/}/auto-pilot-install.XXXXXX")"
ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/refs/heads/${REPO_REF}.tar.gz"
ARCHIVE_PATH="${WORK_DIR}/auto-pilot.tar.gz"
EXTRACT_DIR="${WORK_DIR}/extract"

cleanup() {
  rm -rf "${WORK_DIR}"
}

trap cleanup EXIT

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_cmd curl
require_cmd tar
require_cmd python3

echo "Downloading Auto Pilot from ${REPO_SLUG}@${REPO_REF}..."
curl -fsSL "${ARCHIVE_URL}" -o "${ARCHIVE_PATH}"

mkdir -p "${EXTRACT_DIR}"
tar -xzf "${ARCHIVE_PATH}" -C "${EXTRACT_DIR}"

SOURCE_PLUGIN_DIR="$(find "${EXTRACT_DIR}" -maxdepth 3 -type d -path '*/auto-pilot' | head -n 1)"
if [[ -z "${SOURCE_PLUGIN_DIR}" ]]; then
  echo "Failed to locate auto-pilot plugin contents in downloaded archive." >&2
  exit 1
fi

if [[ ! -f "${SOURCE_PLUGIN_DIR}/.codex-plugin/plugin.json" ]]; then
  echo "Downloaded archive does not contain a valid Codex plugin manifest." >&2
  exit 1
fi

mkdir -p "$(dirname "${INSTALL_DIR}")"
rm -rf "${INSTALL_DIR}"
cp -R "${SOURCE_PLUGIN_DIR}" "${INSTALL_DIR}"

mkdir -p "$(dirname "${MARKETPLACE_PATH}")"

python3 - "${MARKETPLACE_PATH}" "${MARKETPLACE_SOURCE_PATH}" <<'PY'
import json
import pathlib
import sys

marketplace_path = pathlib.Path(sys.argv[1]).expanduser()
source_path = sys.argv[2]

if marketplace_path.exists():
    with marketplace_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
else:
    data = {}

if not isinstance(data, dict):
    raise SystemExit("Marketplace file must contain a JSON object.")

data.setdefault("name", "local-plugins")
interface = data.setdefault("interface", {})
if not isinstance(interface, dict):
    interface = {}
    data["interface"] = interface
interface.setdefault("displayName", "Local Plugins")

plugins = data.setdefault("plugins", [])
if not isinstance(plugins, list):
    raise SystemExit("Marketplace plugins field must be a JSON array.")

entry = {
    "name": "auto-pilot",
    "source": {
        "source": "local",
        "path": source_path,
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Coding",
}

replaced = False
for index, plugin in enumerate(plugins):
    if isinstance(plugin, dict) and plugin.get("name") == "auto-pilot":
        plugins[index] = entry
        replaced = True
        break

if not replaced:
    plugins.append(entry)

marketplace_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
PY

echo "Auto Pilot installed."
echo "Plugin path: ${INSTALL_DIR}"
echo "Marketplace: ${MARKETPLACE_PATH}"
echo "Marketplace source path: ${MARKETPLACE_SOURCE_PATH}"
echo
echo "Restart Codex, then run:"
echo "/auto-pilot:autopilot Build a budgeting app for freelancers"
