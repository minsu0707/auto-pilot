#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_MANIFEST = REPO_ROOT / ".codex-plugin" / "plugin.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_non_empty(data: dict[str, object], key: str) -> object:
    value = data.get(key)
    if value in (None, "", [], {}):
        fail(f"Missing required manifest field: {key}")
    return value


def expect_file(path: Path, label: str) -> None:
    if not path.is_file():
        fail(f"Missing required file for {label}: {path.relative_to(REPO_ROOT)}")


def main() -> None:
    expect_file(PLUGIN_MANIFEST, "plugin manifest")

    try:
        manifest = json.loads(PLUGIN_MANIFEST.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in .codex-plugin/plugin.json: {exc}")

    if not isinstance(manifest, dict):
        fail("plugin.json must contain a top-level object")

    for key in ("name", "version", "description", "type", "skills", "interface", "homepage", "repository", "license"):
        require_non_empty(manifest, key)

    if manifest["type"] != "plugin":
        fail("plugin.json field `type` must equal `plugin`")

    skills_path = REPO_ROOT / str(manifest["skills"])
    if not skills_path.is_dir():
        fail(f"skills directory does not exist: {skills_path.relative_to(REPO_ROOT)}")

    skill_files = sorted(skills_path.glob("*/SKILL.md"))
    if not skill_files:
        fail("skills directory must contain at least one */SKILL.md file")

    skill_dirs = sorted(path for path in skills_path.iterdir() if path.is_dir())
    missing_skill_md = [path.name for path in skill_dirs if not (path / "SKILL.md").is_file()]
    if missing_skill_md:
        fail(f"Every top-level skill directory must contain SKILL.md. Missing in: {', '.join(missing_skill_md)}")

    interface = manifest["interface"]
    if not isinstance(interface, dict):
        fail("plugin.json field `interface` must contain an object")

    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "websiteURL",
        "privacyPolicyURL",
        "termsOfServiceURL",
        "composerIcon",
        "logo",
    ):
        require_non_empty(interface, key)

    capabilities = interface["capabilities"]
    if not isinstance(capabilities, list) or not all(isinstance(item, str) and item for item in capabilities):
        fail("interface.capabilities must be a non-empty list of strings")

    for key in ("composerIcon", "logo"):
        asset_path = REPO_ROOT / str(interface[key])
        expect_file(asset_path, key)

    expect_file(REPO_ROOT / "PRIVACY.md", "privacy policy")
    expect_file(REPO_ROOT / "TERMS.md", "terms of service")

    print("Plugin manifest and skills structure validated.")


if __name__ == "__main__":
    main()
