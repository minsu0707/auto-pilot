#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"


DEFAULT_BLOCKER_POLICY = (
    "retry technical failures automatically, defer low-risk polish, "
    "ask only for secrets, approvals, payments, OAuth, and production launch"
)
DEFAULT_ARCHITECTURE = "Feature-based"
DEFAULT_THEME = "Minimal"
ARCHITECTURE_PRESETS = ("Simple", "Feature-based", "Scalable")
THEME_PRESETS = ("Minimal", "Bold", "Playful", "Premium")

DEFAULT_STACK_SENTINELS = {
    "",
    "default",
    "use defaults",
    "use the defaults",
    "go with defaults",
    "just use the defaults",
    "기본값",
    "기본값으로",
    "기본값으로 해줘",
}


@dataclass(frozen=True)
class Question:
    index: int
    key: str
    label: str
    optional: bool = False


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_question_schema() -> list[Question]:
    schema = load_json(TEMPLATES_DIR / "intake-schema.json")
    ordered = [Question(**item) for item in schema["questionOrder"]]
    optional = [Question(optional=True, **item) for item in schema.get("optionalQuestions", [])]
    return ordered + optional


def intake_state_path(workspace: Path) -> Path:
    return workspace / ".autopilot" / "intake.json"


def intake_summary_path(workspace: Path) -> Path:
    return workspace / ".autopilot" / "intake-summary.json"


def require_intake_state(workspace: Path) -> dict[str, Any]:
    state_path = intake_state_path(workspace)
    if not state_path.exists():
        raise FileNotFoundError(
            "Intake state not found. Start intake first with init_intake.py or autopilot.py start."
        )
    return load_json(state_path)


def load_or_create_intake_state(workspace: Path, initial_prompt: str | None = None) -> dict[str, Any]:
    state_path = intake_state_path(workspace)
    if state_path.exists():
        return load_json(state_path)

    questions = load_question_schema()
    answers = {question.key: "" for question in questions}
    if initial_prompt:
        answers["product_summary"] = initial_prompt.strip()

    state = {
        "questions": [question.__dict__ for question in questions],
        "answers": answers,
        "currentIndex": 2 if answers["product_summary"] else 1,
        "completed": False,
    }
    if not answers["product_summary"]:
        state["currentIndex"] = 1

    save_intake_state(workspace, state)
    return state


def save_intake_state(workspace: Path, state: dict[str, Any]) -> None:
    write_json(intake_state_path(workspace), state)


def unanswered_required_questions(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        question
        for question in state["questions"]
        if not question.get("optional") and not str(state["answers"].get(question["key"], "")).strip()
    ]


def find_current_question(state: dict[str, Any]) -> dict[str, Any] | None:
    for question in state["questions"]:
        if question["index"] < state["currentIndex"]:
            continue
        if str(state["answers"].get(question["key"], "")).strip():
            continue
        return question
    return None


def remaining_questions(state: dict[str, Any], current_question: dict[str, Any] | None) -> int:
    if current_question is None:
        return 0
    return len(
        [
            question
            for question in state["questions"]
            if question["index"] > current_question["index"]
            and not str(state["answers"].get(question["key"], "")).strip()
            and not question.get("optional")
        ]
    )


def format_question(state: dict[str, Any]) -> str:
    question = find_current_question(state)
    if question is None:
        return "All required intake questions are complete."
    remaining = remaining_questions(state, question)
    return f"{question['index']}. {question['label']}\nQuestions remaining: {remaining}"


def record_answer(workspace: Path, answer: str) -> dict[str, Any]:
    state = require_intake_state(workspace)
    question = find_current_question(state)
    if question is None:
        return state

    state["answers"][question["key"]] = answer.strip()
    state["currentIndex"] = question["index"] + 1

    if not unanswered_required_questions(state):
        state["completed"] = True

    save_intake_state(workspace, state)
    return state


def normalize_bool_like(answer: str) -> str:
    text = answer.strip()
    if not text:
        return text
    lowered = text.lower()
    if lowered in {"y", "yes", "필요", "있음", "있어요", "있다"}:
        return "yes"
    if lowered in {"n", "no", "불필요", "없음", "없어요", "없다"}:
        return "no"
    return text


def select_preset(answer: str, presets: tuple[str, ...], default: str) -> str:
    text = answer.strip()
    if not text:
        return default

    lowered = text.lower()
    for preset in presets:
        if preset.lower() in lowered:
            return preset

    return default


def derive_defaults(answers: dict[str, str]) -> dict[str, str]:
    resolved = dict(answers)
    stack_pref = resolved.get("stack_preferences", "").strip()
    if stack_pref.lower() in DEFAULT_STACK_SENTINELS or stack_pref in DEFAULT_STACK_SENTINELS:
        resolved["stack_preferences"] = "Next.js + TypeScript + Tailwind CSS"

    resolved["architecture_preset"] = select_preset(
        resolved.get("architecture_preset", ""),
        ARCHITECTURE_PRESETS,
        DEFAULT_ARCHITECTURE,
    )

    if not resolved.get("deploy_target", "").strip():
        resolved["deploy_target"] = "Vercel"

    if not resolved.get("data_store", "").strip():
        resolved["data_store"] = "Supabase"

    resolved["theme_preset"] = select_preset(
        resolved.get("theme_preset", ""),
        THEME_PRESETS,
        DEFAULT_THEME,
    )

    for key in ("auth_mode", "payments_mode", "admin_required"):
        resolved[key] = normalize_bool_like(resolved.get(key, ""))
        if not resolved[key]:
            resolved[key] = "no"

    if not resolved.get("blocker_policy", "").strip():
        resolved["blocker_policy"] = DEFAULT_BLOCKER_POLICY

    if not resolved.get("design_direction", "").strip():
        resolved["design_direction"] = "No extra design reference provided beyond the selected theme."

    return resolved


def bool_label(value: str) -> str:
    normalized = normalize_bool_like(value)
    if normalized == "yes":
        return "Required"
    if normalized == "no":
        return "Not required"
    return value or "TBD"


def architecture_guidance(value: str) -> str:
    if value == "Simple":
        return "Use a lean MVP-friendly structure with fewer folders and minimal abstraction."
    if value == "Scalable":
        return "Use clearer separation for shared, feature, and app-level concerns so the project can grow without major restructuring."
    return "Organize code primarily by feature or domain, with shared code extracted only when reuse becomes clear."


def theme_guidance(value: str) -> str:
    if value == "Bold":
        return "Use stronger contrast, assertive typography, and more prominent visual hierarchy."
    if value == "Playful":
        return "Use a friendlier, more expressive visual language with softer shapes and lighter tone."
    if value == "Premium":
        return "Use polished spacing, refined hierarchy, and a more upscale, composed presentation."
    return "Use restrained styling, clear spacing, and a calm visual system with low decoration."


def create_spec_markdown(answers: dict[str, str]) -> str:
    return f"""# Project Spec

## Product Summary

{answers['product_summary']}

## Target User

{answers['target_user']}

## Core Features

{answers['core_features']}

## Out of Scope for This Version

{answers['non_goals']}

## Tech Stack

{answers['stack_preferences']}

## Architecture Preset

{answers['architecture_preset']}

{architecture_guidance(answers['architecture_preset'])}

## Operating Constraints

- Authentication: {bool_label(answers['auth_mode'])}
- Payments: {bool_label(answers['payments_mode'])}
- Admin: {bool_label(answers['admin_required'])}
- Deploy Target: {answers['deploy_target']}
- Data Store: {answers['data_store']}

## Theme Preset

{answers['theme_preset']}

{theme_guidance(answers['theme_preset'])}

## Design Direction

{answers['design_direction']}

## Blocker Policy

{answers['blocker_policy']}

## Definition of Done

{answers['definition_of_done']}
"""


def create_progress_markdown(answers: dict[str, str]) -> str:
    return f"""# Progress

## Current Status

- Intake completed
- Spec written
- Autonomous execution ready

## Recently Completed

- Locked the initial project brief
- Locked the definition of done
- Initialized runtime state files

## Notes

- Product summary: {answers['product_summary']}
- Target user: {answers['target_user']}
- Architecture preset: {answers['architecture_preset']}
- Theme preset: {answers['theme_preset']}
"""


def create_next_markdown(answers: dict[str, str]) -> str:
    return f"""# Next Steps

## Immediate

1. Create the initial project structure
2. Break the MVP into milestones based on the core features
3. Implement the first shippable slice

## Implementation Defaults

- Architecture preset: {answers['architecture_preset']}
- Architecture guidance: {architecture_guidance(answers['architecture_preset'])}
- Theme preset: {answers['theme_preset']}
- Theme guidance: {theme_guidance(answers['theme_preset'])}

## Constraints

- Authentication: {bool_label(answers['auth_mode'])}
- Payments: {bool_label(answers['payments_mode'])}
- Admin: {bool_label(answers['admin_required'])}
- Blocker policy: {answers['blocker_policy']}

## Definition of Done Reference

{answers['definition_of_done']}
"""


def create_runtime_state(answers: dict[str, str]) -> dict[str, Any]:
    return {
        "projectName": answers["product_summary"],
        "status": "running",
        "currentMilestone": "Project bootstrap",
        "currentTask": "Set up the initial workspace and first implementation slice",
        "architecturePreset": answers["architecture_preset"],
        "themePreset": answers["theme_preset"],
        "architectureGuidance": architecture_guidance(answers["architecture_preset"]),
        "themeGuidance": theme_guidance(answers["theme_preset"]),
        "retryCount": 0,
        "lastSuccessfulStep": "Locked project spec from intake",
        "definitionOfDoneMet": False,
    }


def create_blockers_state() -> dict[str, Any]:
    return {"active": [], "resolved": []}


def bootstrap_workspace(workspace: Path, intake_answers: dict[str, str]) -> dict[str, Path]:
    answers = derive_defaults(intake_answers)

    docs_dir = workspace / "docs"
    autopilot_dir = workspace / "autopilot"
    ensure_dir(docs_dir)
    ensure_dir(autopilot_dir)

    spec_path = docs_dir / "spec.md"
    progress_path = docs_dir / "progress.md"
    next_path = docs_dir / "next.md"
    state_path = autopilot_dir / "state.json"
    blockers_path = autopilot_dir / "blockers.json"

    spec_path.write_text(create_spec_markdown(answers))
    progress_path.write_text(create_progress_markdown(answers))
    next_path.write_text(create_next_markdown(answers))
    write_json(state_path, create_runtime_state(answers))
    write_json(blockers_path, create_blockers_state())

    summary_path = intake_summary_path(workspace)
    write_json(summary_path, {"answers": answers})

    return {
        "spec": spec_path,
        "progress": progress_path,
        "next": next_path,
        "state": state_path,
        "blockers": blockers_path,
        "summary": summary_path,
    }
