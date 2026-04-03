---
name: auto-pilot
description: Intake-first autonomous project execution for Codex. Use when the user wants a short project request turned into a long-running build workflow with minimal interruptions, or explicitly mentions 오토파일럿/autopilot.
summary: Ask once, lock spec, save state, keep shipping.
metadata:
  priority: 8
  promptSignals:
    phrases:
      - "오토파일럿"
      - "autopilot"
      - "auto-pilot"
      - "24시간 계속"
      - "with ap"
      - "using ap"
    allOf:
      - [ap, build]
      - [build, ap]
      - [ap, make]
      - [make, ap]
      - [ap, create]
      - [create, ap]
      - [ap, app]
      - [app, ap]
      - [ap, 만들어줘]
      - [만들어줘, ap]
    anyOf:
      - "오토파일럿"
      - "autopilot"
      - "auto-pilot"
    minScore: 7
retrieval:
  aliases:
    - 오토파일럿
    - autopilot mode
    - auto-pilot mode
    - with ap
    - intake first execution
    - continuous project execution
  intents:
    - start an autopilot project
    - run intake and keep building
    - continue a project with minimal interruptions
  entities:
    - spec
    - progress
    - blockers
    - state
---

# Auto Pilot

Use this skill as the umbrella workflow for long-running project execution.

## Goal

Turn a short product request into a resumable execution loop that:

- gathers the minimum required inputs once
- locks a written spec and definition of done
- keeps implementing the next highest-priority work
- escalates only for true human-only blockers

## Operating Model

### If state does not exist yet

1. Route to the intake workflow first.
2. Ask only for high-impact decisions.
3. Infer safe defaults for the rest.
4. Write these files:
   - `docs/spec.md`
   - `docs/progress.md`
   - `docs/next.md`
   - `autopilot/state.json`
   - `autopilot/blockers.json`
5. Start implementation immediately after the spec is locked.

### If state already exists

1. Read `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, and `autopilot/blockers.json`.
2. Confirm whether there is an active `human-required` blocker.
3. If not blocked, continue with the top unfinished task.
4. Save results back to the same files after each loop.

## Intake Rules

Ask for only the minimum complete project contract:

- product summary
- target user
- core features
- non-goals for this version
- stack preference or default stack permission
- architecture preset
- auth requirement
- payment requirement
- admin requirement
- deploy target
- data store
- theme preset
- design direction refinement
- blocker policy
- definition of done

Keep the intake compact, but ask exactly one question at a time.
Treat one-question-at-a-time intake as the default behavior, not an optional preference.
For the exact interaction format, follow `../autopilot-intake/SKILL.md`.

## Execution Rules

1. Always choose the smallest shippable slice.
2. Prefer working software over broad scaffolding with no validation.
3. Run relevant verification after each meaningful change.
4. Update progress and next-step files after each loop.
5. Continue automatically after intake unless a true `human-required` blocker is active.
6. Ask the user only when:
   - secrets are required
   - external account setup is required
   - payment or production deployment approval is required
   - the product direction is ambiguous in a way that changes the build materially

## Blocker Policy

### `retryable`

- dependency install errors
- failing tests
- build issues
- small runtime bugs

Behavior:

- retry automatically
- try one or more alternative fixes
- only escalate after retry budget is exhausted

### `deferable`

- placeholder copy
- icon selection
- optional polish
- non-critical analytics

Behavior:

- keep moving with a reasonable default
- write the deferred decision into `docs/next.md` when useful

### `human-required`

- API keys or secrets
- OAuth app creation
- payment account setup
- production deployment approval
- ambiguous product direction that changes scope materially

Behavior:

- stop only at the minimum blocking decision
- ask one focused question
- continue immediately after the answer
