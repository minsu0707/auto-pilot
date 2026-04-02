# Auto Pilot

> Ask once. Lock the brief. Keep shipping.

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

English | [한국어](./README.ko.md) | [日本語](./README.ja.md) | [中文](./README.zh.md) | [العربية](./README.ar.md)

Auto Pilot is a local Codex plugin that turns a short request like `Build me a budgeting app` into an intake-first execution workflow.

Instead of stopping every few steps to ask for missing context, Auto Pilot:

- collects the minimum required inputs once
- saves a reusable project contract
- generates spec, progress, next-step, and runtime state files
- gives Codex a resumable structure for long-running execution

## Why It Exists

Short prompts are convenient, but they are usually too weak for long autonomous work.

Auto Pilot closes that gap by adding:

- one-question-at-a-time intake
- explicit definition of done
- blocker policy
- resumable project state

The goal is simple: less babysitting, more forward motion.

## What It Does

- Converts a short project request into a structured intake session
- Uses a `1. Question` / `Questions remaining: N` UX pattern
- Writes `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, and `autopilot/blockers.json`
- Keeps enough state for the next Codex session to resume from where it stopped
- Ships with a plugin manifest and repo-local marketplace wiring

## Quick Start

Start a new intake session:

```bash
python3 auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

Answer the current question:

```bash
python3 auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

Check the current mode and status:

```bash
python3 auto-pilot/scripts/autopilot.py status \
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

- [auto-pilot](./auto-pilot): plugin root
- [auto-pilot/.codex-plugin/plugin.json](./auto-pilot/.codex-plugin/plugin.json): plugin manifest
- [auto-pilot/scripts](./auto-pilot/scripts): CLI and helper scripts
- [auto-pilot/skills](./auto-pilot/skills): orchestration, intake, and resume skills
- [.agents/plugins/marketplace.json](./.agents/plugins/marketplace.json): repo-local marketplace config

## Current Status

This repository currently focuses on:

- intake UX
- spec and state bootstrapping
- resume-friendly file structure
- multilingual README entry points

The next logical step is a one-command installer that places the plugin into a home-level marketplace automatically.
