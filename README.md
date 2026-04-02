# auto-pilot

Local Codex plugin repository for `Auto Pilot`.

## Languages

- English: `README.md`
- Korean: [`README.ko.md`](/Users/minsu/Documents/Codex/README.ko.md)
- Japanese: [`README.ja.md`](/Users/minsu/Documents/Codex/README.ja.md)
- Chinese: [`README.zh.md`](/Users/minsu/Documents/Codex/README.zh.md)
- Arabic: [`README.ar.md`](/Users/minsu/Documents/Codex/README.ar.md)

## Contents

- [Auto Pilot plugin root](/Users/minsu/Documents/Codex/auto-pilot)
- [Repo-local marketplace config](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- Scripts for intake, state generation, and resume flow

## Core Features

- Turn a short project request into an intake session
- Ask one question at a time
- Use the `1. Question` / `Questions remaining: N` UX pattern
- Generate `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, and `autopilot/blockers.json` after the last answer
- Keep a resumable state structure for later Codex sessions

## Quick Start

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

Then answer one question at a time.

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

Check status:

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py status \
  --workspace /tmp/my-project
```
