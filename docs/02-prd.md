# Auto Pilot PRD

## Product Goal

Let a user start a 0-to-1 software project from a short one-line request and, after a single structured intake, let Codex continue with minimal human intervention.

## User Jobs To Be Done

1. When I describe a product in simple language, the system should convert it into a real build plan.
2. When I am away, the system should keep making progress without avoidable questions.
3. When the system is blocked, it should ask only for the smallest missing decision.
4. When I come back, I should be able to see what is done and what is left at a glance.

## Non-Goals

- Remove all human approval steps from the platform
- Bypass secrets, OAuth setup, payment approval, or deployment permissions
- Run forever without a definition of done
- Replace product judgment completely when the user has provided no direction

## Product Principles

- Ask once at the beginning, not repeatedly
- Use strong defaults in low-risk areas
- Save state after every meaningful step
- Prefer moving forward with placeholders over stopping
- Keep going unless the blocker is truly high risk
- Make progress visible through a small set of files

## User Flow

### 1. Short Request

Example:

`Build a budgeting app for freelancers`

### 2. Structured Intake

The plugin collects the minimum data required for long-running execution.

- product type
- target user
- core features
- out-of-scope items for this version
- preferred stack or permission to use defaults
- architecture preset
- auth requirement and provider
- payment requirement
- admin requirement
- deploy target
- data store and managed provider
- theme preset
- visual vibe
- design direction
- definition of done

### 3. Upfront Integration Setup

If the chosen auth or managed backend needs env values, the plugin switches into a single setup step before execution.

- detect required providers from the intake answers
- check whether the required env values already exist in the project
- ask for the missing values in one consolidated payload
- write only `.env` / `.env.local` and `.env.example`, never docs or runtime state

### 4. Spec Lock

The plugin writes a project brief and execution contract to disk.

For user-facing products, it also writes a dedicated design brief before UI implementation starts.

### 5. Execution Loop

The plugin repeatedly:

1. manager reads state and confirms the real execution backend
2. planner defines the current shippable slice
3. builder implements the smallest shippable slice
4. designer reviews user-facing UI when applicable
5. QA validates the slice
6. manager records progress and chooses the next task

### 6. Blocker Handling

Blockers are classified into:

- `retryable`
- `deferable`
- `human-required`

### 7. Stop Condition

The plugin stops when the full definition of done has been satisfied.

## MVP Scope

### Required

- intake flow
- project brief generation
- task breakdown generation
- persisted runtime state
- resume after interruption
- blocker classification
- definition-of-done tracking

### Strongly Recommended

- GitHub integration
- deployment target integration
- notification channel integration
- preview environment verification

## System Output Files

Files that define a valid existing Auto Pilot project:

- `autopilot/state.json`
- `autopilot/blockers.json`
- `docs/next.md`
- `autopilot/secrets-status.json` when upfront integration setup applies

Files written once setup is complete:

- `docs/spec.md`
- `docs/design.md` for user-facing projects
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`

Files written while setup is still pending:

- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`
- `autopilot/secrets-status.json`

Treat the project as existing if `autopilot/state.json` exists, even when `docs/spec.md` and `docs/progress.md` are not present yet because setup is still pending.

## Functional Requirements

### Intake

- convert a short request into an intake session
- infer defaults where possible
- require explicit input only for high-risk decisions
- persist the captured brief

### Upfront Integration Setup

- detect secret-bearing providers such as Google OAuth and Supabase from intake answers
- read existing `.env` / `.env.local` values before asking the user again
- request missing env values in one consolidated payload
- keep secret values out of `docs/*.md`, `autopilot/state.json`, `autopilot/blockers.json`, and intake summaries
- update `.env.example` with placeholders only

### Planning

- create milestones
- break milestones into executable tasks
- order tasks by dependency and value

### Execution

- always read current state before acting
- let the manager route work through planner, builder, designer, and QA checkpoints
- select the next shippable slice only after planner review
- update code, docs, and config together
- run tests, lint, builds, and browser verification where appropriate
- save state at the end of each loop

### Recovery

- resume from saved state after interruption
- detect repeated failures
- escalate only after the retry budget has been exhausted

### Communication

- summarize status in a human-readable format
- surface the current blocker instead of full execution logs

## Blocker Policy

### Retryable

- dependency install failure
- flaky test
- build misconfiguration
- small runtime bug

Behavior:

- retry automatically
- try alternative fixes
- do not ask the user while retry budget remains

### Deferable

- placeholder copy
- icon choice
- detailed visual polish
- optional analytics

Behavior:

- continue with safe defaults
- record deferred decisions in `docs/next.md`

### Human-Required

- API keys
- OAuth app registration
- payment setup
- domain purchase
- production deployment approval

Behavior:

- use the upfront setup phase first for known integration env values
- pause only the blocked path when external console work or approvals are still missing
- request the smallest necessary action

## Definition of Done

Every project must have an explicit definition of done. Example:

- landing page exists
- authentication works
- core feature A works
- core feature B works
- admin page exists
- tests pass
- app build succeeds
- deploy target is configured
- README explains local run and deployment

## Key Risks

- users may not define done clearly enough
- poor intake design may cause unnecessary questions
- weak state files may cause the autonomous loop to drift
- external approvals still break the illusion of full autonomy

## MVP Success Metrics

- percent of sessions that reach spec lock without rework
- percent of blockers classified correctly without human correction
- percent of successful resumes after interruption
- median number of human interventions per project
- percent of defined tasks completed without additional prompting
