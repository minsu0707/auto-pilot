---
name: autopilot-resume
description: Resume a previously started 오토파일럿 project from saved state files. Use when the user asks to continue, resume, keep going, or finish an existing autopilot project.
summary: Read state, pick the next task, continue execution.
metadata:
  priority: 7
  promptSignals:
    phrases:
      - "오토파일럿 계속"
      - "오토파일럿 재개"
      - "resume autopilot"
      - "continue autopilot"
      - "keep going"
      - "다음 작업 이어서"
    anyOf:
      - "resume"
      - "continue"
      - "재개"
      - "계속"
    minScore: 4
retrieval:
  aliases:
    - 오토파일럿 재개
    - resume autopilot
    - continue execution
  intents:
    - continue a saved project
    - resume from progress files
  entities:
    - spec
    - progress
    - next
    - blockers
---

# Auto Pilot Resume

Use this skill when a project already has saved autopilot state.

## Required Inputs

Read these files first if they exist:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## Resume Workflow

1. Determine whether there is an active blocker.
2. If the blocker is `human-required`, surface only the next minimal action.
3. If not blocked, choose the highest-priority unfinished task.
4. Implement, validate, and update the state files.
5. Stop only if:
   - definition of done is met, or
   - a human-required blocker prevents further work

## Resume Output

Return a concise status update:

- last completed work
- current task
- next task after this
- blocker status
