# Auto Pilot MVP Roadmap

## Phase 1: Lock the Docs

- finalize the product name
- lock the PRD
- define the intake schema
- define the state files
- define the blocker policy

## Phase 2: Plugin Scaffold

- create `plugins/auto-pilot/`
- write `plugin.json`
- add skill folders
- add script placeholders
- add a marketplace entry if needed

## Phase 3: Intake Engine

- detect project-style prompts
- run the minimum intake questions
- write `docs/spec.md`
- write the initial `autopilot/state.json`

## Phase 4: Execution Engine

- choose the next task from current state
- run the implementation loop
- update `docs/progress.md`
- update `docs/next.md`

## Phase 5: Recovery and Alerts

- resume from prior state
- classify blockers
- notify the user only for human-required actions

## Phase 6: Real Project Validation

- test on one real 0-to-1 project
- measure interruption count
- refine intake and blocker policy

## Recommended Build Order

1. Intake
2. State files
3. Next-task selector
4. Blocker classifier
5. Resume flow
6. Notifications
7. Deploy integration

## MVP Exit Criteria

- a short request becomes a saved project brief
- the plugin can resume from saved state
- one realistic project can be pushed through with limited human intervention
- most remaining interruptions are high-risk external actions
