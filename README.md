# Auto Pilot

---

<p align="center">
  <img src="./assets/auto-pilot.png" alt="Auto Pilot mascot" width="260" />
</p>

> Ask once. Lock the brief. Keep shipping.

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

English | [한국어](./README.ko.md) | [日本語](./README.ja.md)

## Install in One Line

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

Use `v0.1.1` for stable installs. Use `develop` only to test upcoming changes.

## Run in Codex

```text
/autopilot Build a budgeting app for freelancers
```

Use `/autopilot` as the primary public entry point.
Restart Codex once after installation so the slash command is loaded.
Install once, then route to intake for new projects and resume automatically for existing ones.
After restart, you can also use the natural-language shortcut `Build a budgeting app for freelancers ap`.

## What It Is

Auto Pilot is a Codex plugin for turning a short product request into a resumable execution workflow.

- Ask for the minimum important inputs once
- Save a reusable project contract
- Keep shipping until a real human-only blocker appears
- Resume later from saved state instead of rediscovering context

## Why It Exists

Short prompts are convenient, but they are usually too weak for long autonomous work.

Auto Pilot closes that gap by adding:

- one-question-at-a-time intake
- explicit definition of done
- blocker policy
- resumable project state

The goal is simple: less babysitting, more forward motion.

## Core Features

- Converts a short project request into a structured intake session
- Uses a `1. Question` / `Questions remaining: N` interaction pattern
- Writes `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, and `autopilot/blockers.json`
- Keeps enough state for the next Codex session to resume from where it stopped
- Keeps canonical plugin code, docs, and installer logic at the repository root

## Quick Start

Start a new intake session:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

Answer the current question:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

Check the current mode and status:

```bash
python3 scripts/autopilot.py status \
  --workspace /tmp/my-project
```

After the final answer, Auto Pilot generates:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. A short prompt starts intake.
2. Auto Pilot asks one question at a time.
3. The answers are normalized into a project contract.
4. Runtime state is created for future execution and resume.
5. Codex can continue from saved files instead of rediscovering context.

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `assets/auto-pilot.png`: mascot image
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: public slash command entry point
- `skills/autopilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates
- `install.sh`: canonical installer
- `uninstall.sh`: canonical uninstaller

## Current Status

This repository root is the canonical plugin root, docs home, and installer home.

For end users, the recommended flow is the one-line installer, one Codex restart, then `/autopilot` inside Codex.
