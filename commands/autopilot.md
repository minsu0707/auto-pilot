---
description: Start or resume Auto Pilot from the current workspace using the provided project prompt.
---

# Auto Pilot

Run the Auto Pilot workflow from the current workspace. Treat `$auto-pilot` as the primary public entry point, with this command available as a secondary plugin command.

## Preflight

Before doing any work:

1. Treat the current workspace as the project root.
2. Check whether these state files already exist:
   - `autopilot/state.json`
   - `autopilot/blockers.json`
   - `autopilot/secrets-status.json`
   - `docs/next.md`
3. Treat `autopilot/state.json` as the primary existing-project signal even when `docs/spec.md` and `docs/progress.md` are not present yet.
4. If `$ARGUMENTS` is empty and no state exists yet, ask the user for a short project prompt before proceeding.
5. If state exists, prefer resume behavior even if the provided prompt is brief.

## Plan

Choose exactly one path:

1. **New project**: no saved state exists
   - Use the slash command arguments as the initial product prompt
   - Route into the intake-first Auto Pilot workflow
   - Ask one question at a time by default
   - Run upfront integration setup after intake when auth or managed services require env values
   - Start implementation automatically after the project contract is locked and required integration setup is complete
2. **Existing project**: saved state exists
   - Read the saved runtime state first
   - If setup is still pending, resume the `setup-secrets` phase instead of implementation
   - Otherwise resume from the highest-priority unfinished task

Keep `$auto-pilot` as the primary public entry point. Intake and resume remain internal routing decisions.

## Commands

Follow the existing Auto Pilot skill behavior rather than inventing new runtime rules.

### New project path

- Use the project prompt from `$ARGUMENTS`
- Apply the workflow defined in `skills/auto-pilot/SKILL.md`
- Use the intake behavior from `skills/autopilot-intake/SKILL.md`
- Collect the minimum required project contract one question at a time
- If required integrations already have env values, write:
  - `docs/spec.md`
  - `docs/design.md` for user-facing projects
  - `docs/progress.md`
  - `docs/next.md`
  - `autopilot/state.json`
  - `autopilot/blockers.json`
  - `autopilot/secrets-status.json`
- If required integrations are missing env values:
  - write `docs/next.md`
  - write `autopilot/state.json`
  - write `autopilot/blockers.json`
  - write `autopilot/secrets-status.json`
  - ask for the consolidated env payload in one step
- Start implementation immediately after the spec is locked and the required env values are present

### Resume path

- Read `autopilot/state.json`, `autopilot/blockers.json`, `autopilot/secrets-status.json`, and `docs/next.md` first
- Apply the resume workflow from `skills/autopilot-resume/SKILL.md`
- If setup is still pending, collect only the missing env payload and treat that as the valid resume target
- If a `human-required` blocker is active, surface only the next minimal action
- Otherwise continue with the top unfinished task and update the same state files

## Verification

Before finishing, confirm the selected path behaved correctly:

- **New project path**
  - intake started from the provided prompt
  - intake either moved into `setup-secrets` or created the execution files immediately
  - implementation moved forward only after required integration setup was complete
- **Resume path**
  - existing state was read
  - setup pending vs execution pending was distinguished correctly
  - blocker status was checked only after setup was complete
  - work resumed from the next unfinished task or the minimal setup/blocker action was surfaced

## Summary

Return a concise status update:

- **Mode**: intake | setup-secrets | resume
- **Prompt**: the user-provided project brief, if present
- **Current task**: what Auto Pilot is doing now
- **Next**: the next task after this step
- **Blocker**: none | setup-pending | retryable | deferable | human-required

## Next Steps

- If intake just started: continue one question at a time until the project contract is locked
- If setup is pending: collect the required env payload in one step before execution
- If work resumed successfully: keep building and validating against the saved definition of done
- If blocked: ask only for the smallest actionable human input
