# Auto Pilot How It Works

## At a Glance

Auto Pilot turns a short product request into a repeatable execution loop.

It does four things in order:

1. route the request into intake or resume
2. lock a project contract on disk
3. route the work through planner, builder, designer, and QA checkpoints
4. recover from interruptions by reading saved state

## End-to-End Flow

```mermaid
flowchart TD
    A["User request"] --> B{"Existing project state?"}
    B -- "No" --> C["Structured intake"]
    B -- "Yes" --> D["Resume from saved state"]
    C --> E["Normalize answers into project contract"]
    E --> F["Write docs/spec.md"]
    E --> G{"User-facing project?"}
    G -- "Yes" --> H["Write docs/design.md"]
    G -- "No" --> I["Skip design brief"]
    F --> J["Create runtime state"]
    H --> J
    I --> J
    D --> J
    J --> K["Manager confirms real execution mode"]
    K --> L["Planner defines the current slice"]
    L --> M["Builder implements"]
    M --> N{"Designer review needed?"}
    N -- "Yes" --> O["Designer reviews UI direction"]
    N -- "No" --> P["QA validates slice"]
    O --> P
    P --> Q{"Blocked?"}
    Q -- "No" --> R["Manager updates progress, next, and state"]
    R --> L
    Q -- "Retryable / Deferable" --> S["Retry or defer with defaults"]
    S --> R
    Q -- "Human-required" --> T["Pause only the blocked path"]
```

## Routing Logic

```mermaid
flowchart LR
    A["Short product request"] --> B{"Spec already locked?"}
    B -- "No" --> C["autopilot-intake"]
    B -- "Yes, work remains" --> D["autopilot-resume"]
    C --> E["auto-pilot orchestration"]
    D --> E["auto-pilot orchestration"]
```

- New requests go through intake first.
- Existing projects skip repeated questions and resume from saved files.
- The public Codex entry point stays `$auto-pilot`.

## Team Model

Auto Pilot uses a manager-led team model.

- `Manager`: owns user interaction and final state updates
- `Planner`: defines the current slice and acceptance criteria
- `Architect`: joins when structure decisions are non-trivial
- `Builder`: implements the current slice
- `Designer`: joins for user-facing UI work
- `QA`: validates the slice before completion

Internal specialist skills back this flow:

- `autopilot-planner`
- `autopilot-architect`
- `autopilot-designer`
- `autopilot-qa`

Manager writes each specialist result back through `scripts/team_checkpoint.py`.

## What Intake Actually Locks

The intake step does not just collect free text. It locks the operating contract for the project.

- product summary
- target user
- core features
- non-goals
- stack preferences
- architecture preset
- theme preset
- visual vibe
- design direction
- deploy target
- data store
- definition of done

These answers become the source of truth for later implementation decisions.

## File Contract

```mermaid
flowchart TD
    A["docs/spec.md"] --> X["Product contract"]
    B["docs/design.md"] --> Y["Design brief for user-facing projects"]
    C["docs/progress.md"] --> Z["What has already been shipped"]
    D["docs/next.md"] --> W["Next execution targets"]
    E["autopilot/state.json"] --> V["Runtime execution state"]
    F["autopilot/blockers.json"] --> U["Active and resolved blockers"]
```

### Always-generated files

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

### Conditional file

- `docs/design.md` for user-facing projects such as landing pages, dashboards, mobile apps, and web apps

## Execution Loop

```mermaid
sequenceDiagram
    participant U as User
    participant A as Manager
    participant P as Planner
    participant B as Builder
    participant D as Designer
    participant Q as QA
    participant S as Saved State
    U->>A: Start or resume project
    A->>S: Read spec, progress, next, state, blockers
    A->>A: Confirm native specialists or downgrade to serial-fallback
    A->>P: Define the next shippable slice
    P-->>A: Slice plan and quality gates
    A->>B: Implement the slice
    alt User-facing UI slice
        B->>D: Hand off for design review
        D-->>A: Design verdict
    end
    A->>Q: Run QA validation
    Q-->>A: Pass/fail verdict
    A->>S: Write progress, next steps, and state
    alt Human-required blocker
        A->>S: Record blocker with ownerRole
        A-->>U: Ask for smallest missing decision
    else No blocker or safe default
        A->>P: Continue loop
    end
```

The execution loop is intentionally conservative:

- always read state before acting
- manager confirms the real backend before dispatching specialists
- planner goes before builder
- QA goes before completion
- keep going with safe defaults where risk is low
- only stop when the definition of done is met or a human-only blocker is unavoidable

## Design Path

For user-facing projects, Auto Pilot adds one extra layer before the first UI build:

1. read `theme_preset`, `visual_vibe`, and `design_direction`
2. create `docs/design.md`
3. use that brief as the active UI direction
4. require one design review pass after the first UI implementation

This is meant to reduce generic SaaS-looking output, not to pretend that every design decision is fully automated.

## Blocker Model

Auto Pilot treats blockers in three buckets, and each blocker should record an `ownerRole`:

- `retryable`: keep trying within the retry budget
- `deferable`: continue with safe defaults and record the follow-up
- `human-required`: pause only the blocked path and ask for the minimum missing input

## Why Resume Works

Resume works because the project is not reconstructed from memory. It is reconstructed from files.

- `docs/spec.md` keeps the contract
- `docs/progress.md` shows completed work
- `docs/next.md` shows the next intended slice
- `autopilot/state.json` tracks runtime context
- `autopilot/blockers.json` explains what is stopping forward motion

That makes session restarts, long gaps, and interrupted runs much cheaper.
