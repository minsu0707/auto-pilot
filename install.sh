#!/usr/bin/env bash

set -euo pipefail

REPO_SLUG="${AUTO_PILOT_REPO_SLUG:-minsu0707/auto-pilot}"
# On develop, keep the default pinned to develop.
# Before cutting a stable release tag, replace this baked-in default with that exact tag.
REPO_REF="${AUTO_PILOT_REPO_REF:-develop}"
INSTALL_DIR="${AUTO_PILOT_INSTALL_DIR:-$HOME/plugins/auto-pilot}"
MARKETPLACE_PATH="${AUTO_PILOT_MARKETPLACE_PATH:-$HOME/.agents/plugins/marketplace.json}"
MARKETPLACE_SOURCE_PATH="${AUTO_PILOT_SOURCE_PATH:-./plugins/auto-pilot}"
CODEX_CONFIG_PATH="${AUTO_PILOT_CODEX_CONFIG_PATH:-$HOME/.codex/config.toml}"
TMP_ROOT="${TMPDIR:-/tmp}"
WORK_DIR="$(mktemp -d "${TMP_ROOT%/}/auto-pilot-install.XXXXXX")"
if [[ "${REPO_REF}" == refs/tags/* ]]; then
  ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/${REPO_REF}.tar.gz"
elif [[ "${REPO_REF}" == refs/heads/* ]]; then
  ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/${REPO_REF}.tar.gz"
elif [[ "${REPO_REF}" == v* ]]; then
  ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/refs/tags/${REPO_REF}.tar.gz"
else
  ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/refs/heads/${REPO_REF}.tar.gz"
fi
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

print_success_art() {
  local image_path="${INSTALL_DIR}/assets/auto-pilot.png"

  if [[ -f "${image_path}" ]]; then
    if command -v imgcat >/dev/null 2>&1; then
      imgcat "${image_path}" || true
      return
    fi

    if command -v chafa >/dev/null 2>&1; then
      chafa --symbols vhalf --size 44x22 "${image_path}" || true
      return
    fi

    if command -v viu >/dev/null 2>&1; then
      viu -w 44 "${image_path}" || true
      return
    fi

    if command -v kitty >/dev/null 2>&1 && [[ "${TERM:-}" == xterm-kitty* ]]; then
      kitty +kitten icat --silent "${image_path}" || true
      return
    fi
  fi

  cat <<'EOF'
      ___   _   _ _____ ___        ____ ___ _     ___ _____
     / _ \ | | | |_   _/ _ \ _____|  _ \_ _| |   / _ \_   _|
    | | | || | | | | || | | |_____| |_) | || |  | | | || |
    | |_| || |_| | | || |_| |     |  __/| || |__| |_| || |
     \__\_\ \___/  |_| \___/      |_|  |___|_____\___/ |_|
EOF
}

echo "Downloading Auto Pilot from ${REPO_SLUG}@${REPO_REF}..."
curl -fsSL "${ARCHIVE_URL}" -o "${ARCHIVE_PATH}"

mkdir -p "${EXTRACT_DIR}"
tar -xzf "${ARCHIVE_PATH}" -C "${EXTRACT_DIR}"

SOURCE_PLUGIN_DIR="$(find "${EXTRACT_DIR}" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "${SOURCE_PLUGIN_DIR}" ]]; then
  echo "Failed to locate extracted repository contents." >&2
  exit 1
fi

if [[ ! -f "${SOURCE_PLUGIN_DIR}/.codex-plugin/plugin.json" ]]; then
  echo "Downloaded archive does not contain a valid Codex plugin manifest." >&2
  exit 1
fi

mkdir -p "$(dirname "${INSTALL_DIR}")"
rm -rf "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

for path in .codex-plugin assets commands docs scripts skills templates README.md README.ko.md README.ja.md README.zh.md README.ar.md install.sh uninstall.sh .gitignore; do
  if [[ -e "${SOURCE_PLUGIN_DIR}/${path}" ]]; then
    cp -R "${SOURCE_PLUGIN_DIR}/${path}" "${INSTALL_DIR}"
  fi
done

mkdir -p "$(dirname "${MARKETPLACE_PATH}")"

python3 - "${MARKETPLACE_PATH}" "${MARKETPLACE_SOURCE_PATH}" "${CODEX_CONFIG_PATH}" <<'PY'
import json
import pathlib
import re
import sys

marketplace_path = pathlib.Path(sys.argv[1]).expanduser()
source_path = sys.argv[2]
config_path = pathlib.Path(sys.argv[3]).expanduser()

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

plugin_ref = f'auto-pilot@{data["name"]}'
header = f'[plugins."{plugin_ref}"]'
block = f'{header}\nenabled = true\n'

config_path.parent.mkdir(parents=True, exist_ok=True)
config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

pattern = re.compile(
    rf'(?ms)^\[plugins\."{re.escape(plugin_ref)}"\]\n(?:.*\n)*?(?=^\[|\Z)'
)

if pattern.search(config_text):
    config_text = pattern.sub(block + "\n", config_text).rstrip() + "\n"
else:
    stripped = config_text.rstrip()
    if stripped:
        config_text = stripped + "\n\n" + block
    else:
        config_text = block

config_path.write_text(config_text, encoding="utf-8")
PY

echo "Auto Pilot installed."
echo "Canonical plugin root: ${INSTALL_DIR}"
echo "Marketplace: ${MARKETPLACE_PATH}"
echo "Marketplace source path: ${MARKETPLACE_SOURCE_PATH}"
echo "Codex config: ${CODEX_CONFIG_PATH}"
echo
print_success_art
echo
echo "🎉 Congratulations! Auto Pilot is installed. Start building now."
echo
echo "Restart Codex, then run:"
echo "\$auto-pilot Build a diary app my friend Dohyeon would love"
echo
echo "Optional shortcut after restart:"
echo "Build a diary app my friend Dohyeon would love ap"
