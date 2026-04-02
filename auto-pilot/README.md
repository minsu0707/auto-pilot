# Auto Pilot Docs

> Ask once. Lock the brief. Keep shipping.

English | [한국어](./docs/i18n/ko.md) | [日本語](./docs/i18n/ja.md) | [中文](./docs/i18n/zh.md) | [العربية](./docs/i18n/ar.md)

## Install in One Line

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## Run in Codex

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

Use `/auto-pilot:autopilot` as the primary public entry point.
Restart Codex once after installation so the slash command is loaded.
Install once, then route to intake for new projects and resume automatically for existing ones.
After restart, you can also use the natural-language shortcut `Build a budgeting app for freelancers ap`.

This folder is the canonical home for the `Auto Pilot` Codex plugin. The plugin turns a short project request into an intake-driven, long-running autonomous execution workflow.

## Files

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: public slash command entry point
- `skills/autopilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Current Status

This folder is the canonical plugin root, docs home, and installer home.

## Usage

You can ask for:

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`
- `Build a budgeting app for freelancers ap`

For new projects, intake follows this UX:

- show one question at a time
- use the `1. Question` format
- show `Questions remaining: N` on the next line
- summarize the captured contract, lock the spec, and start execution after the last answer

## Script Example

```bash
python3 scripts/autopilot.py start \
  --workspace /path/to/project \
  --prompt "Build a budgeting app for freelancers"

python3 scripts/autopilot.py answer \
  --workspace /path/to/project \
  --text "Freelancers and solo business owners"

python3 scripts/autopilot.py status \
  --workspace /path/to/project
```

After the final answer, the plugin generates:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

Lower-level scripts remain available:

- `init_intake.py`
- `record_answer.py`
- `status.py`

For end users, the recommended flow is the one-line installer, one Codex restart, then `/auto-pilot:autopilot` inside Codex.
