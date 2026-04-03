---
description: Start or resume Auto Pilot from the current workspace using the provided project prompt.
---

# Auto Pilot

Run the Auto Pilot workflow from the current workspace. Treat `$auto-pilot` as the primary public entry point, with this command available as a secondary plugin command.

## Preflight

Before doing any work:

1. Treat the current workspace as the project root.
2. Check whether these state files already exist:
   - `docs/spec.md`
   - `docs/progress.md`
   - `docs/next.md`
   - `autopilot/state.json`
   - `autopilot/blockers.json`
3. If `$ARGUMENTS` is empty and no state exists yet, ask the user for a short project prompt before proceeding.
4. If state exists, prefer resume behavior even if the provided prompt is brief.

## Plan

Choose exactly one path:

1. **New project**: no saved state exists
   - Use the slash command arguments as the initial product prompt
   - Route into the intake-first Auto Pilot workflow
   - Ask one question at a time by default
   - Start implementation automatically after the project contract is locked
2. **Existing project**: saved state exists
   - Read the saved state files
   - Resume from the highest-priority unfinished task

Keep `$auto-pilot` as the primary public entry point. Intake and resume remain internal routing decisions.

## Commands

Follow the existing Auto Pilot skill behavior rather than inventing new runtime rules.

### New project path

- Use the project prompt from `$ARGUMENTS`
- Apply the workflow defined in `skills/auto-pilot/SKILL.md`
- Use the intake behavior from `skills/autopilot-intake/SKILL.md`
- Collect the minimum required project contract one question at a time
- Write:
  - `docs/spec.md`
  - `docs/progress.md`
  - `docs/next.md`
  - `autopilot/state.json`
  - `autopilot/blockers.json`
- Start implementation immediately after the spec is locked without waiting for extra user confirmation

### Resume path

- Read the existing state files first
- Apply the resume workflow from `skills/autopilot-resume/SKILL.md`
- If a `human-required` blocker is active, surface only the next minimal action
- Otherwise continue with the top unfinished task and update the same state files

## Verification

Before finishing, confirm the selected path behaved correctly:

- **New project path**
  - intake started from the provided prompt
  - state files were created or updated
  - implementation moved forward after spec lock
- **Resume path**
  - existing state was read
  - blocker status was checked
  - work resumed from the next unfinished task or the minimal blocker was surfaced

## Summary

Return a concise status update:

- **Mode**: intake | resume
- **Prompt**: the user-provided project brief, if present
- **Current task**: what Auto Pilot is doing now
- **Next**: the next task after this step
- **Blocker**: none | retryable | deferable | human-required

## Next Steps

- If intake just started: continue one question at a time until the project contract is locked
- If work resumed successfully: keep building and validating against the saved definition of done
- If blocked: ask only for the smallest actionable human input
