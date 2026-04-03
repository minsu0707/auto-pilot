#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
DEFAULT_VIBE = "Calm"
ARCHITECTURE_PRESETS = ("Simple", "Feature-based", "Scalable")
THEME_PRESETS = ("Minimal", "Bold", "Playful", "Premium")
VIBE_PRESETS = ("Editorial", "Playful", "Premium", "Calm", "Techy")

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
    resolved["visual_vibe"] = select_preset(
        resolved.get("visual_vibe", ""),
        VIBE_PRESETS,
        default_vibe_for_theme(resolved["theme_preset"]),
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


def default_vibe_for_theme(value: str) -> str:
    if value == "Bold":
        return "Techy"
    if value == "Playful":
        return "Playful"
    if value == "Premium":
        return "Premium"
    return DEFAULT_VIBE


def theme_guidance(value: str) -> str:
    if value == "Bold":
        return "Use stronger contrast, assertive typography, and more prominent visual hierarchy."
    if value == "Playful":
        return "Use a friendlier, more expressive visual language with softer shapes and lighter tone."
    if value == "Premium":
        return "Use polished spacing, refined hierarchy, and a more upscale, composed presentation."
    return "Use restrained styling, clear spacing, and a calm visual system with low decoration."


def vibe_guidance(value: str) -> str:
    if value == "Editorial":
        return "Favor strong layout composition, confident whitespace, and typography-led presentation over generic dashboard chrome."
    if value == "Playful":
        return "Use softer corners, friendlier shapes, warmer accents, and more expressive UI moments without becoming childish."
    if value == "Premium":
        return "Use refined hierarchy, richer surfaces, elegant contrast, and restrained motion that feels polished."
    if value == "Techy":
        return "Use sharper contrast, structured layout rhythm, and a more product-forward feel with crisp visual hierarchy."
    return "Keep the interface calm, spacious, and restrained with low decoration and clear hierarchy."


def is_user_facing_project(answers: dict[str, str]) -> bool:
    corpus = " ".join(
        [
            answers.get("product_summary", ""),
            answers.get("core_features", ""),
            answers.get("target_user", ""),
            answers.get("definition_of_done", ""),
        ]
    ).lower()
    positive_signals = (
        "landing",
        "marketing",
        "dashboard",
        "admin",
        "ui",
        "ux",
        "web",
        "app",
        "mobile",
        "page",
        "screen",
        "consumer",
        "site",
        "saas",
        "portal",
        "일기",
        "가계부",
        "앱",
        "화면",
        "페이지",
        "대시보드",
        "랜딩",
        "모바일",
    )
    negative_signals = (
        "cli",
        "sdk",
        "library",
        "package",
        "api only",
        "backend only",
        "worker",
        "daemon",
        "batch",
        "headless",
    )
    if matches_any_signal(corpus, positive_signals):
        return True
    if matches_any_signal(corpus, negative_signals):
        return False
    return normalize_bool_like(answers.get("admin_required", "")) == "yes"


def matches_any_signal(corpus: str, signals: tuple[str, ...]) -> bool:
    for signal in signals:
        if re.search(r"[a-z]", signal):
            if re.search(rf"\b{re.escape(signal)}\b", corpus):
                return True
        elif signal in corpus:
            return True
    return False


def select_design_sources(answers: dict[str, str]) -> list[str]:
    summary = " ".join(
        [answers.get("product_summary", ""), answers.get("core_features", "")]
    ).lower()
    sources = ["frontend-ui-ux skill"]
    if "figma.com" in summary or "node-id=" in summary:
        sources.append("Figma reference if provided")
        return sources
    if any(token in summary for token in ("landing", "marketing", "brand", "promo", "homepage", "랜딩")):
        sources.extend(["Land-book", "Page Collective"])
    else:
        sources.extend(["Mobbin", "Refero"])
    if answers.get("visual_vibe") in {"Editorial", "Premium"} and "Page Collective" not in sources:
        sources.append("Page Collective")
    return sources[:4]


def target_reference_summary(answers: dict[str, str]) -> str:
    sources = select_design_sources(answers)
    if "Figma reference if provided" in sources:
        return "Prioritize Figma if available, then use curated references to sharpen hierarchy and layout decisions before the first UI build."
    if "Land-book" in sources:
        return "Review landing-page inspiration for composition, headline rhythm, and visual storytelling instead of defaulting to generic SaaS hero blocks."
    return "Review product UI inspiration for app structure, dashboard density, and component tone before implementing the first screen."


def color_direction(answers: dict[str, str]) -> str:
    theme = answers["theme_preset"]
    vibe = answers["visual_vibe"]
    if theme == "Bold" or vibe == "Techy":
        return "High-contrast neutrals with one assertive accent; avoid washed-out grays and low-energy palettes."
    if theme == "Playful" or vibe == "Playful":
        return "Warm or cheerful accents with softer neutrals; keep contrast accessible and avoid rainbow overload."
    if theme == "Premium" or vibe == "Premium":
        return "Restrained palette with richer dark neutrals, refined highlights, and limited accent usage."
    if vibe == "Editorial":
        return "Minimal palette driven by typography and whitespace; use color sparingly for emphasis."
    return "Calm neutral foundation with one muted accent and clean contrast boundaries."


def typography_direction(answers: dict[str, str]) -> str:
    vibe = answers["visual_vibe"]
    if vibe == "Editorial":
        return "Typography should carry the design with stronger scale contrast and more intentional heading rhythm."
    if vibe == "Premium":
        return "Use refined, elegant type hierarchy with comfortable line lengths and higher perceived polish."
    if vibe == "Techy":
        return "Use crisp, structured typography with stronger information density and sharper hierarchy."
    if vibe == "Playful":
        return "Use approachable, friendly type scale with slightly softer rhythm and less rigid structure."
    return "Use restrained, highly readable typography with modest but clear hierarchy."


def spacing_direction(answers: dict[str, str]) -> str:
    vibe = answers["visual_vibe"]
    if vibe in {"Editorial", "Premium"}:
        return "Prefer spacious layouts with stronger breathing room and deliberate negative space."
    if vibe == "Techy":
        return "Use balanced-to-compact spacing with a clear grid and tidy alignment."
    if vibe == "Playful":
        return "Use balanced spacing with softer grouping and slightly rounder visual rhythm."
    return "Keep spacing clean and calm with consistent vertical rhythm."


def component_tone(answers: dict[str, str]) -> str:
    vibe = answers["visual_vibe"]
    if vibe == "Techy":
        return "Components should feel crisp and product-driven, with clearer borders, tighter grouping, and stronger state emphasis."
    if vibe == "Premium":
        return "Components should feel polished and upscale, with subtle surfaces and restrained visual noise."
    if vibe == "Playful":
        return "Components should feel friendly and expressive, with softer shapes and warmer micro-details."
    if vibe == "Editorial":
        return "Components should defer to layout and typography; avoid over-decorated cards and heavy widget framing."
    return "Components should stay minimal and unobtrusive, supporting clarity over decoration."


def layout_pattern(answers: dict[str, str]) -> str:
    summary = answers["product_summary"].lower()
    if any(token in summary for token in ("landing", "marketing", "brand", "promo", "homepage", "랜딩")):
        return "Use a composition-first marketing layout with more variation in section rhythm and stronger visual pacing."
    if any(token in summary for token in ("dashboard", "admin", "portal", "대시보드", "관리")):
        return "Use a structured app shell with clear navigation, prioritized overview panels, and fewer throwaway cards."
    return "Use a product-focused app layout with strong hierarchy, intentional empty space, and one standout primary screen."


def motion_guidance(answers: dict[str, str]) -> str:
    vibe = answers["visual_vibe"]
    if vibe in {"Premium", "Editorial"}:
        return "Use restrained motion: soft fades, measured reveals, and subtle transitions."
    if vibe == "Playful":
        return "Use a few friendly transitions and small expressive moments, but avoid noisy micro-animation."
    if vibe == "Techy":
        return "Use crisp transitions that reinforce responsiveness and hierarchy without adding clutter."
    return "Keep motion subtle and purposeful, limited to structure and focus changes."


def avoid_list(answers: dict[str, str]) -> list[str]:
    items = [
        "Generic SaaS dashboard cards with no visual hierarchy",
        "Default-feeling Tailwind layouts with interchangeable sections",
        "Flat monochrome UI with no focal point",
    ]
    vibe = answers["visual_vibe"]
    if vibe == "Editorial":
        items.append("Over-framing every section with boxes and widget chrome")
    if vibe == "Playful":
        items.append("Turning expressive styling into toy-like UI noise")
    if vibe == "Techy":
        items.append("Low-contrast pastel styling that weakens product clarity")
    return items


def design_review_focus(answers: dict[str, str]) -> str:
    vibe = answers["visual_vibe"]
    if vibe == "Editorial":
        return "Check typography hierarchy, section rhythm, and whether the layout still feels intentional without over-relying on cards."
    if vibe == "Premium":
        return "Check polish, spacing, and whether the visual hierarchy feels upscale rather than merely minimal."
    if vibe == "Playful":
        return "Check whether the UI feels warm and expressive without slipping into clutter."
    if vibe == "Techy":
        return "Check product clarity, contrast, and whether the interface looks confident instead of generic."
    return "Check that the UI feels calm and intentional rather than plain or unfinished."


def create_design_markdown(answers: dict[str, str]) -> str:
    sources = select_design_sources(answers)
    avoid = "\n".join(f"- {item}" for item in avoid_list(answers))
    return f"""# Design Brief

## Theme Preset

{answers['theme_preset']}

## Visual Vibe

{answers['visual_vibe']}

## User-Facing Classification

This project is treated as a user-facing product, so design synthesis is required before implementing the first UI.

## Research Execution Status

This brief is the initial direction synthesized from intake answers and local project docs.
Review the planned research stack below and refine this brief before implementing the first production UI.

## Planned Design Research Stack

- Local design skill: `frontend-ui-ux`
- Product docs: `docs/01-product-brief.md`, `docs/02-prd.md`, `docs/03-plugin-spec.md`, `docs/04-mvp-roadmap.md`
- Curated inspiration sources: {", ".join(sources)}

## Initial Reference Direction

{target_reference_summary(answers)}

## Color Direction

{color_direction(answers)}

## Typography Direction

{typography_direction(answers)}

## Spacing and Density

{spacing_direction(answers)}

## Component Tone

{component_tone(answers)}

## Layout Pattern

{layout_pattern(answers)}

## Motion Guidance

{motion_guidance(answers)}

## Design Direction Refinement

{answers['design_direction']}

## Avoid

{avoid}

## Review Requirement

Run one explicit post-build design review after the first UI pass. {design_review_focus(answers)}
"""


def create_spec_markdown(answers: dict[str, str]) -> str:
    design_reference = (
        "Treat `docs/design.md` as the binding design brief for any user-facing UI implementation."
        if is_user_facing_project(answers)
        else "No dedicated design brief is required unless the project later grows a user-facing interface."
    )
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

## Visual Vibe

{answers['visual_vibe']}

{vibe_guidance(answers['visual_vibe'])}

## Design Direction

{design_reference}

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
- Visual vibe: {answers['visual_vibe']}
- Design synthesis: {"Required before UI implementation" if is_user_facing_project(answers) else "Skipped for non-user-facing project"}
"""


def create_next_markdown(answers: dict[str, str]) -> str:
    design_line = (
        "1. Review the planned design sources and refine docs/design.md before building the first UI slice\n"
        "2. Create the initial project structure\n"
        "3. Break the MVP into milestones based on the core features\n"
        "4. Implement the first shippable slice using docs/design.md as the design brief\n"
        "5. Run one post-build design review after the first UI pass"
        if is_user_facing_project(answers)
        else
        "1. Create the initial project structure\n"
        "2. Break the MVP into milestones based on the core features\n"
        "3. Implement the first shippable slice"
    )
    return f"""# Next Steps

## Immediate

{design_line}

## Implementation Defaults

- Architecture preset: {answers['architecture_preset']}
- Architecture guidance: {architecture_guidance(answers['architecture_preset'])}
- Theme preset: {answers['theme_preset']}
- Theme guidance: {theme_guidance(answers['theme_preset'])}
- Visual vibe: {answers['visual_vibe']}
- Vibe guidance: {vibe_guidance(answers['visual_vibe'])}
- Design brief: {"docs/design.md" if is_user_facing_project(answers) else "Not required for this project type"}

## Constraints

- Authentication: {bool_label(answers['auth_mode'])}
- Payments: {bool_label(answers['payments_mode'])}
- Admin: {bool_label(answers['admin_required'])}
- Blocker policy: {answers['blocker_policy']}

## Definition of Done Reference

{answers['definition_of_done']}
"""


def create_runtime_state(answers: dict[str, str]) -> dict[str, Any]:
    user_facing = is_user_facing_project(answers)
    sources = select_design_sources(answers)
    return {
        "projectName": answers["product_summary"],
        "status": "running",
        "currentMilestone": "Project bootstrap",
        "currentTask": (
            "Synthesize the design brief and set up the first implementation slice"
            if user_facing
            else "Set up the initial workspace and first implementation slice"
        ),
        "architecturePreset": answers["architecture_preset"],
        "themePreset": answers["theme_preset"],
        "visualVibe": answers["visual_vibe"],
        "architectureGuidance": architecture_guidance(answers["architecture_preset"]),
        "themeGuidance": theme_guidance(answers["theme_preset"]),
        "vibeGuidance": vibe_guidance(answers["visual_vibe"]),
        "userFacingProject": user_facing,
        "designResearchSummary": (
            f"Review {'/'.join(sources)} and refine docs/design.md before the first UI implementation."
            if user_facing
            else "No dedicated design synthesis required for this project type."
        ),
        "designReviewRequired": user_facing,
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
    design_path = docs_dir / "design.md"
    progress_path = docs_dir / "progress.md"
    next_path = docs_dir / "next.md"
    state_path = autopilot_dir / "state.json"
    blockers_path = autopilot_dir / "blockers.json"

    spec_path.write_text(create_spec_markdown(answers))
    if is_user_facing_project(answers):
        design_path.write_text(create_design_markdown(answers))
    progress_path.write_text(create_progress_markdown(answers))
    next_path.write_text(create_next_markdown(answers))
    write_json(state_path, create_runtime_state(answers))
    write_json(blockers_path, create_blockers_state())

    summary_path = intake_summary_path(workspace)
    write_json(summary_path, {"answers": answers})

    return {
        "spec": spec_path,
        "design": design_path,
        "progress": progress_path,
        "next": next_path,
        "state": state_path,
        "blockers": blockers_path,
        "summary": summary_path,
    }
