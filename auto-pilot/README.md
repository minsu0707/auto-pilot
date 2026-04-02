# Auto Pilot Docs

> Ask once. Lock the brief. Keep shipping.

English | [한국어](./docs/i18n/ko.md) | [日本語](./docs/i18n/ja.md) | [中文](./docs/i18n/zh.md) | [العربية](./docs/i18n/ar.md)

This folder contains the initial documentation package for the `Auto Pilot` Codex plugin. The plugin turns a short project request into an intake-driven, long-running autonomous execution workflow.

## Files

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
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

This folder is the plugin root. The repo-local marketplace is wired through [marketplace.json](../.agents/plugins/marketplace.json).

## Usage

You can ask for:

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`

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

## Start in One Line

For a copy-paste friendly start command, use:

```bash
python3 scripts/autopilot.py start --workspace /path/to/project --prompt "Build a budgeting app for freelancers"
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

The current session may not refresh the plugin list immediately. Reopening the workspace in a new session is the safest way to force plugin discovery.
