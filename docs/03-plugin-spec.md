# Auto Pilot Plugin Spec

## Plugin Role

Auto Pilot is not a single tool. It is an orchestration layer on top of Codex with five core responsibilities.

- intake
- planning
- execution
- recovery
- blocker handling

For a visual walkthrough of the full request-to-resume flow, see [`docs/05-how-it-works.md`](./05-how-it-works.md).

## Proposed Structure

```text
repo-root/
  .codex-plugin/plugin.json
  assets/
  docs/
  commands/
  skills/
    auto-pilot/SKILL.md
    autopilot-intake/SKILL.md
    autopilot-resume/SKILL.md
  scripts/
    autopilot.py
    autopilot_lib.py
    init_intake.py
    record_answer.py
    status.py
  templates/
    provider-secrets.json
  install.sh
  uninstall.sh
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
- `autopilot/state.json` exists and work is incomplete, so the request should route to resume even if setup is still pending

## State Contract

### State Files That Define An Existing Project

- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json` when upfront integration setup applies
- `docs/next.md`

Treat the project as existing if `autopilot/state.json` exists, even when `docs/spec.md` and `docs/progress.md` are not present yet.

### Files Written Once Setup Is Complete

- `docs/spec.md`
- `docs/design.md` for user-facing projects
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`

### Files Written While Setup Is Pending

- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`

### `autopilot/state.json`

Recommended shape:

```json
{
  "projectName": "Auto Pilot",
  "status": "running",
  "currentMilestone": "MVP foundation",
  "currentTask": "Manager: confirm execution mode and dispatch Planner",
  "executionMode": "team-product",
  "teamRoles": ["Manager", "Planner", "Builder", "Designer", "QA"],
  "currentOwner": "Manager",
  "qualityGates": ["Planner checkpoint", "Designer checkpoint", "QA checkpoint"],
  "lastPlannerCheckpoint": "Pending initial planner pass.",
  "lastReviewerVerdict": "Pending QA review",
  "lastRoleResults": {},
  "setupStatus": "complete | pending",
  "requiredIntegrations": ["google-oauth", "supabase"],
  "secretsReady": true,
  "retryCount": 0,
  "lastSuccessfulStep": "Created project brief",
  "definitionOfDoneMet": false
}
```

When upfront integration setup is still pending, the same file should remain present with:

- `status: "setup-pending"`
- `currentMilestone: "Integration setup"`
- `currentTask` pointing at the missing env payload

### `autopilot/blockers.json`

Recommended shape:

```json
{
  "active": [],
  "resolved": [],
  "entryContract": {
    "ownerRole": "Manager | Planner | Architect | Builder | Designer | QA",
    "classification": "retryable | deferable | human-required",
    "summary": "Short blocker summary"
  }
}
```

### `autopilot/secrets-status.json`

Recommended shape:

```json
{
  "requiredProviders": ["google-oauth", "supabase"],
  "envFilePath": "/workspace/.env.local",
  "requiredKeys": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
  "presentKeys": ["GOOGLE_CLIENT_ID"],
  "missingKeys": ["GOOGLE_CLIENT_SECRET"],
  "setupChecklist": [
    {
      "providerId": "google-oauth",
      "displayName": "Google OAuth",
      "items": ["Create the OAuth client"],
      "docsLinks": ["https://console.cloud.google.com/apis/credentials"]
    }
  ],
  "status": "pending | complete"
}
```

### Runtime checkpoint helper

Use `scripts/team_checkpoint.py` to persist planner, architect, builder, designer, QA, and manager results back into:

- `docs/progress.md`
- `docs/next.md`
- `docs/design.md` when relevant
- `autopilot/state.json`
- `autopilot/blockers.json`

This helper applies after execution has started. It is not the mechanism for collecting upfront integration env values.

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
- `architecture_preset`
- `theme_preset`
- `visual_vibe`
- `design_direction`
- `deploy_target`
- `data_store`
- `definition_of_done`

The `auth_mode` and `data_store` answers should remain provider-aware so the setup phase can detect required integrations.

## Execution Rules

1. Always read state before acting.
2. Do not ask a question if a safe default is allowed by policy.
3. Before execution begins, detect required integrations and complete the upfront env setup phase if needed.
4. Manager must confirm the real backend first: native specialist agents when available, otherwise `serial-fallback`.
5. Route work through the manager-led team in this order: planner → builder → QA, with architect/designer added only when needed.
6. Prefer the smallest shippable slice.
7. Always validate after implementation.
8. Save state after each loop.
9. Stop only when the definition of done is met or a `human-required` blocker is active.

Treat `setupStatus: "pending"` as a normal pre-execution phase, not as a blocker entry by itself.

For user-facing projects, generate `docs/design.md` before implementing the first UI and treat it as the active design brief.

## Recommended Integrations

- GitHub: issues, PRs, and commit visibility
- Vercel: deployment and preview verification
- Notification provider: blocker alerts
- Optional docs or project tracking integration
