# Auto Pilot

## One-Line Summary

Auto Pilot is a Codex plugin that turns a short request such as "build me an app" into a long-running autonomous project workflow after collecting the minimum required setup details once.

## Core Idea

Most users do not want to write a long technical spec themselves. They want to make a short request, answer a small set of startup questions, and then let Codex keep implementing and validating the project with minimal interruption.

## Problem Statement

- A short prompt does not contain enough structure for long autonomous execution
- Codex often stops too early and asks too many follow-up questions
- Most interruptions are caused by missing requirements, weak defaults, or no blocker policy
- Users want Codex to behave like a project executor, not only a chat assistant

## Product Promise

Auto Pilot collects the minimum required project inputs at the start, locks the spec and the definition of done, and keeps moving until one of these is true:

- the definition of done has been satisfied
- a truly human-only blocker has been reached

## Primary Users

- solo founders
- non-technical operators
- product-minded builders
- developers who want Codex to run as a long-duration project system

## Success Criteria

- a short request expands into a structured intake session
- execution can resume after the session ends because the state is saved
- human intervention is limited to secrets, approvals, payments, OAuth, and deployment
- users can understand current state and next steps without reading raw execution logs
