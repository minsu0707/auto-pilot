# Auto Pilot Docs

English | [한국어](./README.ko.md) | [日本語](./README.ja.md) | [中文](./README.zh.md) | [العربية](./README.ar.md)

This folder contains the initial documentation package for the `Auto Pilot` Codex plugin. The plugin turns a short project request into an intake-driven, long-running autonomous execution workflow.

## Files

- `01-product-brief.md`: product overview
- `02-prd.md`: functional requirements and operating model
- `03-plugin-spec.md`: plugin structure and state model
- `04-mvp-roadmap.md`: MVP implementation sequence
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

This folder is the plugin root. The repo-local marketplace is wired through [marketplace.json](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json).

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
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py start \
  --workspace /path/to/project \
  --prompt "Build a budgeting app for freelancers"

python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py answer \
  --workspace /path/to/project \
  --text "Freelancers and solo business owners"

python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py status \
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

The current session may not refresh the plugin list immediately. Reopening the workspace in a new session is the safest way to force plugin discovery.
