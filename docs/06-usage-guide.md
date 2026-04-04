# Auto Pilot Usage Guide

## Who This Is For

Use this guide when you want to:

- install Auto Pilot into Codex
- start a brand-new project from a short prompt
- resume an existing Auto Pilot project
- understand which files Auto Pilot writes
- understand how manager, planner, builder, designer, and QA fit together

## Recommended Public Entry Point

Stable `v0.1.1`:

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

Use `/auto-pilot:autopilot` when you installed the current stable tag.

Preview on `develop`:

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

Use `$auto-pilot` only when you intentionally installed the unreleased `develop` line.
On `develop`, the plugin command in `commands/autopilot.md` remains a secondary path behind `$auto-pilot`.

## Install

### Stable

Stable `v0.1.1` expects `curl`, `tar`, and `python3`.

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

Use the stable tag when you want the currently published release line.

### Develop

Use `develop` only when you intentionally want the next unreleased behavior for testing.

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/develop/install.sh | env -u NO_COLOR bash
```

## First Run in Codex

This guide documents the current `main` workflow. If you stay on stable `v0.1.1`, use the stable path below. Features such as `docs/design.md` land on the preview line first and ship in the next stable release.

1. Install Auto Pilot from the stable tag or `develop`.
2. Restart Codex once so the skill loads.
3. Run the command that matches the line you installed.

Stable example:

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

Preview example:

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

## What Happens on a New Project

Auto Pilot does not immediately start coding from the first sentence.
It first locks a project contract through intake.

### Intake Flow

Auto Pilot asks one question at a time in this format:

```text
6. What project structure should I use? Simple, Feature-based, or Scalable?
Questions remaining: 9
```

The intake currently locks:

1. product summary
2. target user
3. core features
4. non-goals
5. stack preferences
6. architecture preset
7. auth requirement and provider
8. payments requirement
9. admin requirement
10. deploy target
11. data store and managed provider
12. theme preset
13. visual vibe
14. design direction
15. definition of done

### After the Final Answer

Auto Pilot now checks whether the selected auth or managed services need upfront env values.

If no env values are needed, or they are already present, Auto Pilot writes:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`

For user-facing projects, it also writes:

- `docs/design.md`

If required env values are missing, Auto Pilot switches to `setup-secrets` first and writes:

- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`
- `.env.example`

At that point you submit the missing values in one payload with:

```bash
./scripts/autopilot secrets \
  --workspace /tmp/my-project \
  --text 'GOOGLE_CLIENT_ID=...'
```

These CLI commands are for local plugin development or debugging.
Run them from the Auto Pilot repository root or the installed plugin directory.
For normal usage inside Codex, prefer `$auto-pilot` or `/auto-pilot:autopilot`.

## What Each File Means

### `docs/spec.md`

The locked project contract.
This is the source of truth for:

- scope
- stack
- architecture preset
- design direction
- quality gates
- definition of done

### `docs/design.md`

Created only for user-facing projects.
This is the active design brief for:

- theme preset
- visual vibe
- UI tone
- layout direction
- design review notes

### `docs/progress.md`

What has already been decided or completed.
This is where role-level progress should accumulate:

- planner notes
- architect notes
- builder progress
- designer notes
- QA verdict

### `docs/next.md`

The next handoff document.
This should tell the next loop:

- planner intent
- builder target
- architect guardrails when needed
- designer notes when needed
- QA checks

### `autopilot/state.json`

The runtime state.
It tracks:

- execution mode
- setup status
- required integrations
- secrets readiness
- active team roles
- current owner
- quality gates
- last planner checkpoint
- last reviewer verdict
- last role results

When setup is still pending, `status` becomes `setup-pending` and the current task points at the consolidated env payload.

### `autopilot/blockers.json`

The blocker registry.
Each blocker should carry:

- `ownerRole`
- `classification`
- `summary`

### `autopilot/secrets-status.json`

The upfront integration setup status.
It tracks:

- required providers
- chosen env file path
- required keys
- present keys
- missing keys
- provider setup checklist
- setup status

## Team Execution Model

Auto Pilot uses a manager-led model.

### Roles

- `Manager`: owns user interaction and final routing
- `Planner`: defines the current slice
- `Architect`: joins when structure decisions are non-trivial
- `Builder`: implements the slice
- `Designer`: reviews user-facing UI work
- `QA`: validates before the slice is treated as complete

### Execution Modes

- `team-product`
  - user-facing or operationally complex projects
- `team-lite`
  - smaller CLI, backend, library, or utility projects
- `serial-fallback`
  - same role order, but executed without native specialist sub-agents

### Role Order

Auto Pilot follows this order:

1. planner
2. architect when needed
3. builder
4. designer when needed
5. QA
6. manager update

Builder should not go first.
QA should not be skipped.
Designer review should not be skipped for user-facing UI slices.

## Resume Behavior

If the project already has saved state files, Auto Pilot should resume instead of starting intake again.

It reads:

- `docs/spec.md`
- `docs/design.md` when present
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

Then it checks:

- current owner
- blocker status
- pending quality gates
- last reviewer verdict

## Blocker Rules

Auto Pilot treats blockers in three classes:

- `retryable`
  - retry automatically within reasonable limits
- `deferable`
  - continue with safe defaults and log the follow-up
- `human-required`
  - ask only for the smallest missing decision

The goal is to pause only the blocked path, not the whole project.

## CLI Scripts

These scripts are useful for local testing and debugging.
Run them from the Auto Pilot repository root or the installed plugin directory.

### Start intake

```bash
./scripts/autopilot start \
  --workspace /tmp/my-project \
  --prompt "Build a diary app my friend Dohyeon would love"
```

### Answer intake

```bash
./scripts/autopilot answer \
  --workspace /tmp/my-project \
  --text "Teenagers who want a cozy, private diary they can decorate every day"
```

### Check status

```bash
./scripts/autopilot status \
  --workspace /tmp/my-project
```

### Submit upfront integration secrets

```bash
./scripts/autopilot secrets \
  --workspace /tmp/my-project \
  --text 'GOOGLE_CLIENT_ID=...'
```

### Alternate answer helper

```bash
python3 scripts/record_answer.py \
  --workspace /tmp/my-project \
  --answer "Use the default stack"
```

## Team Checkpoint Script

Use this only when you are explicitly driving or testing the internal manager-led flow.

Example planner checkpoint:

```bash
python3 scripts/team_checkpoint.py \
  --workspace /tmp/my-project \
  --role planner \
  --summary "Planner locked the first slice." \
  --planner-checkpoint "Milestone 1 is locked." \
  --planner-intent "Deliver the first working slice." \
  --builder-target "Implement auth shell and entry creation." \
  --qa-check "Sign-in works." \
  --next-owner Builder \
  --next-task "Builder: implement the first slice."
```

This script updates:

- `docs/progress.md`
- `docs/next.md`
- `docs/design.md` when relevant
- `autopilot/state.json`
- `autopilot/blockers.json`

## Recommended Reading Order

If you want to understand the system in depth:

1. `docs/06-usage-guide.md`
2. `docs/05-how-it-works.md`
3. `docs/03-plugin-spec.md`
4. `docs/02-prd.md`

## Common Mental Model

Think of Auto Pilot like this:

- intake locks the contract
- saved files become the source of truth
- manager routes work through role checkpoints
- blockers stay explicit
- resume continues from files, not memory
