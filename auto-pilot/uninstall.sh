#!/usr/bin/env bash

set -euo pipefail

INSTALL_DIR="${AUTO_PILOT_INSTALL_DIR:-$HOME/plugins/auto-pilot}"
MARKETPLACE_PATH="${AUTO_PILOT_MARKETPLACE_PATH:-$HOME/.agents/plugins/marketplace.json}"
CODEX_CONFIG_PATH="${AUTO_PILOT_CODEX_CONFIG_PATH:-$HOME/.codex/config.toml}"

rm -rf "${INSTALL_DIR}"

python3 - "${MARKETPLACE_PATH}" "${CODEX_CONFIG_PATH}" <<'PY'
import json
import pathlib
import re
import sys

marketplace_path = pathlib.Path(sys.argv[1]).expanduser()
config_path = pathlib.Path(sys.argv[2]).expanduser()
if not marketplace_path.exists():
    marketplace_name = "local-plugins"
else:
    with marketplace_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    marketplace_name = data.get("name", "local-plugins")
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

plugin_ref = f'auto-pilot@{marketplace_name}'
header_pattern = re.compile(
    rf'(?ms)^\[plugins\."{re.escape(plugin_ref)}"\]\n(?:.*\n)*?(?=^\[|\Z)'
)

if config_path.exists():
    config_text = config_path.read_text(encoding="utf-8")
    config_text = header_pattern.sub("", config_text)
    config_text = re.sub(r"\n{3,}", "\n\n", config_text).strip()
    if config_text:
        config_text += "\n"
    config_path.write_text(config_text, encoding="utf-8")
PY

echo "Auto Pilot removed from ${INSTALL_DIR}"
echo "Marketplace updated: ${MARKETPLACE_PATH}"
echo "Codex config updated: ${CODEX_CONFIG_PATH}"
