---
name: autopilot
description: Intake-first autonomous project execution for Codex. Use when the user wants a short project request turned into a long-running build workflow with minimal interruptions, or explicitly mentions 오토파일럿/autopilot.
summary: Ask once, lock spec, save state, keep shipping.
metadata:
  priority: 8
  promptSignals:
    phrases:
      - "오토파일럿"
      - "autopilot"
      - "한번만 물어보고 계속"
      - "중간에 묻지 말고 끝까지"
      - "24시간 계속"
      - "brief once"
      - "ask once"
      - "keep building"
      - "keep shipping"
      - "계속 진행해줘"
    allOf:
      - [한번만, 물어보고, 계속]
      - [중간에, 묻지, 말고]
      - [ask, once]
      - [keep, building]
    anyOf:
      - "오토파일럿"
      - "autopilot"
      - "계속"
      - "끝까지"
      - "24시간"
    minScore: 5
retrieval:
  aliases:
    - 오토파일럿
    - autopilot mode
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
- auth requirement
- payment requirement
- admin requirement
- deploy target
- data store
- design direction
- blocker policy
- definition of done

Keep the intake compact. Prefer one grouped message instead of repeated back-and-forth.
For the exact interaction format, follow `../autopilot-intake/SKILL.md`.

## Execution Rules

1. Always choose the smallest shippable slice.
2. Prefer working software over broad scaffolding with no validation.
3. Run relevant verification after each meaningful change.
4. Update progress and next-step files after each loop.
5. Ask the user only when:
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

- continue with safe defaults
- record the deferred item in `docs/next.md`

### `human-required`

- API keys
- OAuth provider setup
- payment activation
- domain purchase
- production go-live approval

Behavior:

- pause only the blocked path
- ask for the smallest actionable input

## Output Expectations

- Keep status legible.
- Summaries should focus on:
  - what changed
  - what is next
  - whether a blocker exists
- Stop when the definition of done is satisfied.
