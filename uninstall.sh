#!/usr/bin/env bash

set -euo pipefail

INSTALL_DIR="${AUTO_PILOT_INSTALL_DIR:-$HOME/.codex/plugins/auto-pilot}"
MARKETPLACE_PATH="${AUTO_PILOT_MARKETPLACE_PATH:-$HOME/.agents/plugins/marketplace.json}"

rm -rf "${INSTALL_DIR}"

python3 - "${MARKETPLACE_PATH}" <<'PY'
import json
import pathlib
import sys

marketplace_path = pathlib.Path(sys.argv[1]).expanduser()
if not marketplace_path.exists():
    raise SystemExit(0)

with marketplace_path.open("r", encoding="utf-8") as handle:
    data = json.load(handle)

plugins = data.get("plugins")
if isinstance(plugins, list):
    data["plugins"] = [
        plugin
        for plugin in plugins
        if not (isinstance(plugin, dict) and plugin.get("name") == "auto-pilot")
    ]

marketplace_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
PY

echo "Auto Pilot removed from ${INSTALL_DIR}"
echo "Marketplace updated: ${MARKETPLACE_PATH}"
