# Auto Pilot Plugin Spec

## Plugin Role

Auto Pilot is not a single tool. It is an orchestration layer on top of Codex with five core responsibilities.

- intake
- planning
- execution
- recovery
- blocker handling

## Proposed Structure

```text
plugins/auto-pilot/
  .codex-plugin/plugin.json
  skills/
    project-intake/SKILL.md
    project-execution/SKILL.md
    blocker-triage/SKILL.md
    resume-from-state/SKILL.md
    done-check/SKILL.md
  scripts/
    bootstrap-state.ts
    choose-next-task.ts
    classify-blocker.ts
    summarize-status.ts
  hooks.json
  .mcp.json
  .app.json
  assets/
```

## Responsibility Split

### `project-intake`

- detect short project requests
- run intake questions
- save the project brief
- lock the definition of done

### `project-execution`

- read current state
- choose the next task
- implement and validate
- update progress and next files

### `blocker-triage`

- classify blockers
- decide whether to retry, defer, or escalate

### `resume-from-state`

- continue after timeouts, session restarts, or repeated automation runs

### `done-check`

- decide whether execution should continue or stop

## Hook Strategy

Hooks should handle routing only, not heavy logic.

### Example Triggers

- the user prompt contains `build`, `make`, `create`, `launch`, `ship`, or equivalent phrasing
- the request looks like project creation, not a single isolated fix
- no locked spec exists yet, so the request should route to intake
- a spec exists and work is incomplete, so the request should route to resume

## State Contract

### Required Files

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

### `autopilot/state.json`

Recommended shape:

```json
{
  "projectName": "Auto Pilot",
  "status": "running",
  "currentMilestone": "MVP foundation",
  "currentTask": "Set up Next.js app shell",
  "retryCount": 0,
  "lastSuccessfulStep": "Created project brief",
  "definitionOfDoneMet": false
}
```

### `autopilot/blockers.json`

Recommended shape:

```json
{
  "active": [],
  "resolved": []
}
```

## Intake Data Model

Recommended fields:

- `product_summary`
- `target_user`
- `core_features`
- `non_goals`
- `stack_preferences`
- `auth_mode`
- `payments_mode`
- `admin_required`
- `design_direction`
- `deploy_target`
- `data_store`
- `blocker_policy`
- `definition_of_done`

## Execution Rules

1. Always read state before acting.
2. Do not ask a question if a safe default is allowed by policy.
3. Prefer the smallest shippable slice.
4. Always validate after implementation.
5. Save state after each loop.
6. Stop only when the definition of done is met or a `human-required` blocker is active.

## Recommended Integrations

- GitHub: issues, PRs, and commit visibility
- Vercel: deployment and preview verification
- Notification provider: blocker alerts
- Optional docs or project tracking integration
