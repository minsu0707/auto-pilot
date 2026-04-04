#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
ENV_ASSIGNMENT_RE = re.compile(r"^\s*(?:export\s+)?([A-Z0-9_]+)\s*=\s*(.*)\s*$")


DEFAULT_BLOCKER_POLICY = (
    "retry technical failures automatically, defer low-risk polish, "
    "collect required integration env values in one upfront setup step, "
    "then ask only for approvals, payments, OAuth console work, and production launch"
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


@dataclass(frozen=True)
class ProviderSecretSpec:
    id: str
    display_name: str
    required_env_vars: list[str]
    optional_env_vars: list[str]
    input_labels: dict[str, str]
    validation_rules: dict[str, dict[str, str]]
    setup_checklist: list[str]
    docs_links: list[str]


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


def load_provider_registry() -> list[dict[str, Any]]:
    registry = load_json(TEMPLATES_DIR / "provider-secrets.json")
    return registry.get("providers", [])


def intake_state_path(workspace: Path) -> Path:
    return workspace / ".autopilot" / "intake.json"


def intake_summary_path(workspace: Path) -> Path:
    return workspace / ".autopilot" / "intake-summary.json"


def runtime_state_path(workspace: Path) -> Path:
    return workspace / "autopilot" / "state.json"


def blockers_state_path(workspace: Path) -> Path:
    return workspace / "autopilot" / "blockers.json"


def secrets_status_path(workspace: Path) -> Path:
    return workspace / "autopilot" / "secrets-status.json"


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
        resolved["stack_preferences"] = "Next.js + TypeScript + Tailwind CSS + shadcn/ui"

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


def is_requirement_enabled(value: str) -> bool:
    normalized = normalize_bool_like(value)
    return bool(normalized) and normalized != "no"


def choose_env_file(workspace: Path, answers: dict[str, str]) -> Path:
    stack = answers.get("stack_preferences", "").lower()
    if any(token in stack for token in ("next.js", "nextjs", "vite", "react")):
        return workspace / ".env.local"
    return workspace / ".env"


def env_example_path(workspace: Path) -> Path:
    return workspace / ".env.example"


def candidate_env_paths(workspace: Path, target_env_path: Path) -> list[Path]:
    ordered = [target_env_path, workspace / ".env.local", workspace / ".env"]
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in ordered:
        if path in seen:
            continue
        unique.append(path)
        seen.add(path)
    return unique


def parse_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if value and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_env_text(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = ENV_ASSIGNMENT_RE.match(line)
        if not match:
            raise ValueError(f"Invalid env line: {line}")
        key = match.group(1)
        value = match.group(2)
        if " #" in value:
            value = value.split(" #", 1)[0]
        values[key] = parse_env_value(value)
    return values


def parse_secret_input(text: str) -> dict[str, str]:
    stripped = text.strip()
    if not stripped:
        return {}
    if stripped.startswith("{"):
        payload = json.loads(stripped)
        if not isinstance(payload, dict):
            raise ValueError("Secret JSON payload must be an object.")
        return {str(key): str(value) for key, value in payload.items() if str(value).strip()}
    parsed = parse_env_text(stripped)
    if not parsed:
        raise ValueError("Secret payload must contain KEY=value lines or a JSON object.")
    return parsed


def read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return parse_env_text(path.read_text())


def read_existing_env_values(workspace: Path, target_env_path: Path) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in candidate_env_paths(workspace, target_env_path):
        for key, value in read_env_file(path).items():
            if key not in merged and value.strip():
                merged[key] = value.strip()
    return merged


def serialize_env_value(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_./:@%+=,-]+", value):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def merge_env_values(path: Path, values: dict[str, str], overwrite_existing: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_text = path.read_text() if path.exists() else ""
    lines = existing_text.splitlines()
    managed_keys = list(values.keys())
    seen_keys: set[str] = set()
    updated_lines: list[str] = []

    for line in lines:
        match = ENV_ASSIGNMENT_RE.match(line)
        if not match:
            updated_lines.append(line)
            continue
        key = match.group(1)
        if key not in values:
            updated_lines.append(line)
            continue

        seen_keys.add(key)
        current_value = parse_env_value(match.group(2))
        if overwrite_existing or not current_value.strip():
            updated_lines.append(f"{key}={serialize_env_value(values[key])}")
        else:
            updated_lines.append(line)

    missing_keys = [key for key in managed_keys if key not in seen_keys]
    if missing_keys and updated_lines:
        updated_lines.append("")
    for key in missing_keys:
        updated_lines.append(f"{key}={serialize_env_value(values[key])}")

    path.write_text("\n".join(updated_lines).rstrip() + "\n")


def placeholder_for_env_key(key: str) -> str:
    return f"your-{key.lower().replace('_', '-')}"


def matches_provider_rule(answer_value: str, match_terms: list[str]) -> bool:
    normalized = answer_value.lower()
    return any(term.lower() in normalized for term in match_terms)


def provider_spec_from_entry(entry: dict[str, Any]) -> ProviderSecretSpec:
    return ProviderSecretSpec(
        id=entry["id"],
        display_name=entry.get("displayName", entry["id"]),
        required_env_vars=list(entry.get("requiredEnvVars", [])),
        optional_env_vars=list(entry.get("optionalEnvVars", [])),
        input_labels=dict(entry.get("inputLabels", {})),
        validation_rules=dict(entry.get("validationRules", {})),
        setup_checklist=list(entry.get("setupChecklist", [])),
        docs_links=list(entry.get("docsLinks", [])),
    )


def detect_required_providers(answers: dict[str, str]) -> list[ProviderSecretSpec]:
    matches: list[ProviderSecretSpec] = []
    for entry in load_provider_registry():
        rules = entry.get("triggerRules", [])
        for rule in rules:
            field = rule.get("field", "")
            value = answers.get(field, "").strip()
            if value and matches_provider_rule(value, list(rule.get("matchAny", []))):
                matches.append(provider_spec_from_entry(entry))
                break
    unique: list[ProviderSecretSpec] = []
    seen: set[str] = set()
    for provider in matches:
        if provider.id in seen:
            continue
        unique.append(provider)
        seen.add(provider.id)
    return unique


def validate_secret_value(key: str, value: str, provider: ProviderSecretSpec) -> str | None:
    rule = provider.validation_rules.get(key, {})
    kind = rule.get("kind", "non-empty")
    if kind == "url" and not re.match(r"^https?://", value):
        return f"{key} must be a valid http(s) URL."
    if not value.strip():
        return f"{key} cannot be empty."
    return None


def validate_secret_payload(payload: dict[str, str], providers: list[ProviderSecretSpec]) -> list[str]:
    errors: list[str] = []
    provider_by_key = {
        key: provider
        for provider in providers
        for key in provider.required_env_vars + provider.optional_env_vars
    }
    for key, value in payload.items():
        provider = provider_by_key.get(key)
        if provider is None:
            continue
        error = validate_secret_value(key, value, provider)
        if error:
            errors.append(error)
    return errors


def required_secret_keys(providers: list[ProviderSecretSpec]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for provider in providers:
        for key in provider.required_env_vars:
            if key in seen:
                continue
            keys.append(key)
            seen.add(key)
    return keys


def secret_input_labels(providers: list[ProviderSecretSpec]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for provider in providers:
        labels.update(provider.input_labels)
    return labels


def build_secrets_status(
    workspace: Path,
    answers: dict[str, str],
    providers: list[ProviderSecretSpec],
) -> dict[str, Any]:
    env_path = choose_env_file(workspace, answers)
    existing_values = read_existing_env_values(workspace, env_path)
    required_keys = required_secret_keys(providers)
    present_keys = [key for key in required_keys if existing_values.get(key, "").strip()]
    missing_keys = [key for key in required_keys if key not in present_keys]
    setup_checklist = [
        {
            "providerId": provider.id,
            "displayName": provider.display_name,
            "items": provider.setup_checklist,
            "docsLinks": provider.docs_links,
        }
        for provider in providers
    ]
    return {
        "requiredProviders": [provider.id for provider in providers],
        "envFilePath": str(env_path),
        "requiredKeys": required_keys,
        "presentKeys": present_keys,
        "missingKeys": missing_keys,
        "inputLabels": secret_input_labels(providers),
        "setupChecklist": setup_checklist,
        "status": "complete" if not missing_keys else "pending",
    }


def setup_pending_message(secret_status: dict[str, Any]) -> str:
    labels = secret_status.get("inputLabels", {})
    lines = [
        "Integration setup is required before execution can start.",
        f"Target env file: {secret_status['envFilePath']}",
        "Accepted formats:",
        "- KEY=value",
        '- {"KEY":"value"}',
        "Missing values:",
    ]
    for key in secret_status.get("missingKeys", []):
        label = labels.get(key, key)
        lines.append(f"- {key}: {label}")
    lines.append("")
    lines.append("Provider checklist:")
    for provider in secret_status.get("setupChecklist", []):
        lines.append(f"- {provider['displayName']}:")
        for item in provider.get("items", []):
            lines.append(f"  - {item}")
        for link in provider.get("docsLinks", []):
            lines.append(f"  - Docs: {link}")
    return "\n".join(lines)


def bool_label(value: str) -> str:
    normalized = normalize_bool_like(value)
    if normalized == "yes":
        return "Required"
    if normalized == "no":
        return "Not required"
    if normalized:
        return f"Required ({value})"
    return value or "TBD"


def architecture_guidance(value: str) -> str:
    if value == "Simple":
        return "Use a lean MVP-friendly structure with fewer folders and minimal abstraction."
    if value == "Scalable":
        return "Use clearer separation for shared, feature, and app-level concerns so the project can grow without major restructuring."
    return "Organize code primarily by feature or domain, with shared code extracted only when reuse becomes clear."


def execution_mode_for_answers(answers: dict[str, str]) -> str:
    override = os.environ.get("AUTO_PILOT_EXECUTION_MODE", "").strip()
    if override in {"team-lite", "team-product", "serial-fallback"}:
        return override

    user_facing = is_user_facing_project(answers)
    architecture = answers["architecture_preset"]
    operational_surface = any(is_requirement_enabled(answers.get(key, "")) for key in ("auth_mode", "payments_mode", "admin_required"))

    return "team-product" if (user_facing or architecture == "Scalable" or operational_surface) else "team-lite"


def team_roles_for_answers(answers: dict[str, str], execution_mode: str) -> list[str]:
    roles = ["Manager", "Planner"]
    if answers["architecture_preset"] == "Scalable":
        roles.append("Architect")
    roles.append("Builder")
    if is_user_facing_project(answers):
        roles.append("Designer")
    roles.append("QA")
    return roles


def quality_gates_for_answers(answers: dict[str, str]) -> list[str]:
    gates = [
        "Planner checkpoint: next slice matches the locked spec and definition of done.",
        "Builder checkpoint: implement the smallest shippable slice without drifting from the agreed structure.",
        "QA checkpoint: run relevant validation, regression checks, and definition-of-done alignment review.",
    ]
    if answers["architecture_preset"] == "Scalable":
        gates.insert(
            1,
            "Architect checkpoint: confirm folder boundaries, shared-vs-feature split, and integration seams before large scaffolding.",
        )
    if is_user_facing_project(answers):
        gates.insert(
            -1,
            "Designer checkpoint: strengthen docs/design.md before the first UI build and run one explicit post-build design review.",
        )
    return gates


def team_mode_summary(execution_mode: str) -> str:
    if execution_mode == "serial-fallback":
        return "Use the manager-led role sequence in a single loop because specialist sub-agents are unavailable in this environment."
    if execution_mode == "team-product":
        return "Run manager-led specialist orchestration for a product surface that benefits from planner, builder, designer, and QA checkpoints."
    return "Run a lighter manager-led team with planner, builder, and QA, adding specialists only when the current slice requires them."


def planner_checkpoint(answers: dict[str, str]) -> str:
    return (
        "Break the locked spec into milestones, define the current slice, and set acceptance criteria before implementation starts."
    )


def planner_checkpoint_seed() -> str:
    return "Pending initial planner pass."


def builder_target(answers: dict[str, str]) -> str:
    target = "Build the next smallest shippable slice from docs/next.md"
    if is_user_facing_project(answers):
        return f"{target}, following docs/design.md as the binding UI brief."
    return f"{target}, following the structure and constraints already locked in docs/spec.md."


def designer_notes(answers: dict[str, str]) -> str:
    if not is_user_facing_project(answers):
        return ""
    return (
        "Designer owns docs/design.md, strengthens the visual brief before the first UI slice, "
        "and runs one explicit design review after the first UI implementation."
    )


def qa_verdict_seed(answers: dict[str, str]) -> str:
    checks = ["spec alignment", "definition of done"]
    if is_user_facing_project(answers):
        checks.insert(0, "design brief alignment")
    return f"Pending. QA must validate {', '.join(checks)} before the slice can be marked complete."


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
    execution_mode = execution_mode_for_answers(answers)
    roles = team_roles_for_answers(answers, execution_mode)
    quality_gates = "\n".join(f"- {gate}" for gate in quality_gates_for_answers(answers))
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

## Execution Mode

{execution_mode}

{team_mode_summary(execution_mode)}

## Team Roles

{", ".join(roles)}

## Quality Gates

{quality_gates}

## Blocker Policy

{answers['blocker_policy']}

## Definition of Done

{answers['definition_of_done']}
"""


def create_progress_markdown(answers: dict[str, str]) -> str:
    execution_mode = execution_mode_for_answers(answers)
    return f"""# Progress

## Current Status

- Intake completed
- Spec written
- Team orchestration ready

## Execution Mode

- Mode: {execution_mode}
- Roles: {", ".join(team_roles_for_answers(answers, execution_mode))}

## Recently Completed

- Locked the initial project brief
- Locked the definition of done
- Initialized team-aware runtime state files

## Planner Notes

- Pending initial planner pass. Planner must break the locked spec into milestones, define the current slice, and set acceptance criteria.

## Builder Progress

- Waiting for planner output before the first implementation slice starts.

## Designer Notes

- {designer_notes(answers) or "No dedicated designer role is active for this project type."}

## QA Verdict

- {qa_verdict_seed(answers)}

## Notes

- Product summary: {answers['product_summary']}
- Target user: {answers['target_user']}
- Architecture preset: {answers['architecture_preset']}
- Theme preset: {answers['theme_preset']}
- Visual vibe: {answers['visual_vibe']}
- Design synthesis: {"Required before UI implementation" if is_user_facing_project(answers) else "Skipped for non-user-facing project"}
"""


def create_next_markdown(answers: dict[str, str]) -> str:
    execution_mode = execution_mode_for_answers(answers)
    quality_gates = "\n".join(f"- {gate}" for gate in quality_gates_for_answers(answers))
    designer_handoff = (
        f"## Designer Notes\n\n- {designer_notes(answers)}\n\n"
        if is_user_facing_project(answers)
        else ""
    )
    return f"""# Next Steps

## Execution Mode

{execution_mode}

## Planner Intent

- {planner_checkpoint(answers)}

## Builder Target

- {builder_target(answers)}

{designer_handoff}## QA Checks

{quality_gates}

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


def create_setup_pending_next_markdown(answers: dict[str, str], secret_status: dict[str, Any]) -> str:
    provider_lines: list[str] = []
    labels = secret_status.get("inputLabels", {})
    provider_specs = {provider.id: provider for provider in detect_required_providers(answers)}
    for provider in secret_status.get("setupChecklist", []):
        provider_spec = provider_specs.get(provider["providerId"])
        provider_lines.append(f"## {provider['displayName']}")
        provider_lines.append("")
        provider_lines.append(f"- Env file: {secret_status['envFilePath']}")
        if provider_spec:
            for key in provider_spec.required_env_vars:
                if key not in secret_status.get("missingKeys", []):
                    continue
                provider_lines.append(f"- Missing {key}: {labels.get(key, key)}")
        for item in provider.get("items", []):
            provider_lines.append(f"- {item}")
        for link in provider.get("docsLinks", []):
            provider_lines.append(f"- Docs: {link}")
        provider_lines.append("")
    provider_block = "\n".join(provider_lines).strip()
    return f"""# Next Steps

## Execution Mode

setup-secrets

## Integration Setup

- Intake is complete, but execution is paused until the required external integration values are available.
- Target env file: {secret_status['envFilePath']}
- Required providers: {", ".join(secret_status['requiredProviders'])}
- Missing keys: {", ".join(secret_status['missingKeys']) or "None"}
- Accepted input formats: `KEY=value` lines or a JSON object

{provider_block}

## Definition of Done Reference

{answers['definition_of_done']}
"""


def create_runtime_state(
    answers: dict[str, str],
    setup_status: str = "complete",
    required_integrations: list[str] | None = None,
    secrets_ready: bool = True,
) -> dict[str, Any]:
    user_facing = is_user_facing_project(answers)
    sources = select_design_sources(answers)
    execution_mode = execution_mode_for_answers(answers)
    roles = team_roles_for_answers(answers, execution_mode)
    quality_gates = quality_gates_for_answers(answers)
    return {
        "projectName": answers["product_summary"],
        "status": "running",
        "currentMilestone": "Project bootstrap",
        "currentTask": "Manager: confirm execution mode, dispatch Planner, and lock the first slice handoff.",
        "executionMode": execution_mode,
        "teamRoles": roles,
        "currentOwner": "Manager",
        "qualityGates": quality_gates,
        "lastPlannerCheckpoint": planner_checkpoint_seed(),
        "lastReviewerVerdict": qa_verdict_seed(answers),
        "lastRoleResults": {},
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
        "setupStatus": setup_status,
        "requiredIntegrations": required_integrations or [],
        "secretsReady": secrets_ready,
    }


def create_blockers_state() -> dict[str, Any]:
    return {
        "active": [],
        "resolved": [],
        "entryContract": {
            "ownerRole": "Manager | Planner | Architect | Builder | Designer | QA",
            "classification": "retryable | deferable | human-required",
            "summary": "Short blocker summary",
        },
    }


def create_setup_pending_state(answers: dict[str, str], secret_status: dict[str, Any]) -> dict[str, Any]:
    state = create_runtime_state(
        answers,
        setup_status="pending",
        required_integrations=list(secret_status.get("requiredProviders", [])),
        secrets_ready=False,
    )
    state["status"] = "setup-pending"
    state["currentMilestone"] = "Integration setup"
    state["currentTask"] = "Manager: collect the required external integration values before execution can start."
    state["lastSuccessfulStep"] = "Locked intake and paused for upfront integration setup"
    return state


def bootstrap_workspace(workspace: Path, intake_answers: dict[str, str]) -> dict[str, Path]:
    answers = derive_defaults(intake_answers)
    providers = detect_required_providers(answers)
    secret_status = build_secrets_status(workspace, answers, providers)

    docs_dir = workspace / "docs"
    autopilot_dir = workspace / "autopilot"
    ensure_dir(docs_dir)
    ensure_dir(autopilot_dir)

    spec_path = docs_dir / "spec.md"
    design_path = docs_dir / "design.md"
    progress_path = docs_dir / "progress.md"
    next_path = docs_dir / "next.md"
    state_path = runtime_state_path(workspace)
    blockers_path = blockers_state_path(workspace)
    secrets_path = secrets_status_path(workspace)

    spec_path.write_text(create_spec_markdown(answers))
    if is_user_facing_project(answers):
        design_path.write_text(create_design_markdown(answers))
    progress_path.write_text(create_progress_markdown(answers))
    next_path.write_text(create_next_markdown(answers))
    write_json(
        state_path,
        create_runtime_state(
            answers,
            setup_status="complete",
            required_integrations=[provider.id for provider in providers],
            secrets_ready=True,
        ),
    )
    write_json(blockers_path, create_blockers_state())
    write_json(secrets_path, secret_status)
    merge_env_values(
        env_example_path(workspace),
        {key: placeholder_for_env_key(key) for key in secret_status.get("requiredKeys", [])},
        overwrite_existing=True,
    )

    summary_path = intake_summary_path(workspace)
    write_json(summary_path, {"answers": answers})

    return {
        "spec": spec_path,
        "design": design_path,
        "progress": progress_path,
        "next": next_path,
        "state": state_path,
        "blockers": blockers_path,
        "secrets": secrets_path,
        "summary": summary_path,
    }


def prepare_workspace_after_intake(workspace: Path, intake_answers: dict[str, str]) -> dict[str, Any]:
    answers = derive_defaults(intake_answers)
    summary_path = intake_summary_path(workspace)
    write_json(summary_path, {"answers": answers})

    providers = detect_required_providers(answers)
    secret_status = build_secrets_status(workspace, answers, providers)

    if secret_status["status"] == "complete":
        outputs = bootstrap_workspace(workspace, answers)
        return {"mode": "execution", "outputs": outputs}

    docs_dir = workspace / "docs"
    autopilot_dir = workspace / "autopilot"
    ensure_dir(docs_dir)
    ensure_dir(autopilot_dir)

    next_path = docs_dir / "next.md"
    next_path.write_text(create_setup_pending_next_markdown(answers, secret_status))

    state_path = runtime_state_path(workspace)
    blockers_path = blockers_state_path(workspace)
    secrets_path = secrets_status_path(workspace)
    write_json(state_path, create_setup_pending_state(answers, secret_status))
    write_json(blockers_path, create_blockers_state())
    write_json(secrets_path, secret_status)
    merge_env_values(
        env_example_path(workspace),
        {key: placeholder_for_env_key(key) for key in secret_status.get("requiredKeys", [])},
        overwrite_existing=True,
    )

    return {
        "mode": "setup-secrets",
        "outputs": {
            "next": next_path,
            "state": state_path,
            "blockers": blockers_path,
            "secrets": secrets_path,
            "summary": summary_path,
        },
        "message": setup_pending_message(secret_status),
    }


def require_intake_summary_answers(workspace: Path) -> dict[str, str]:
    summary_path = intake_summary_path(workspace)
    if not summary_path.exists():
        raise FileNotFoundError("Intake summary not found. Complete intake before submitting secrets.")
    summary = load_json(summary_path)
    answers = summary.get("answers")
    if not isinstance(answers, dict):
        raise FileNotFoundError("Intake summary is missing answers.")
    return {str(key): str(value) for key, value in answers.items()}


def submit_secrets(workspace: Path, text: str) -> dict[str, Any]:
    answers = require_intake_summary_answers(workspace)
    providers = detect_required_providers(answers)
    if not providers:
        outputs = bootstrap_workspace(workspace, answers)
        return {"mode": "execution", "outputs": outputs}

    payload = parse_secret_input(text)
    validation_errors = validate_secret_payload(payload, providers)
    if validation_errors:
        raise ValueError("\n".join(validation_errors))

    env_path = choose_env_file(workspace, answers)
    relevant_updates = {
        key: value
        for key, value in payload.items()
        if key in set(required_secret_keys(providers))
    }
    if relevant_updates:
        merge_env_values(env_path, relevant_updates, overwrite_existing=False)

    secret_status = build_secrets_status(workspace, answers, providers)
    write_json(secrets_status_path(workspace), secret_status)
    merge_env_values(
        env_example_path(workspace),
        {key: placeholder_for_env_key(key) for key in secret_status.get("requiredKeys", [])},
        overwrite_existing=True,
    )

    if secret_status["status"] == "complete":
        outputs = bootstrap_workspace(workspace, answers)
        return {"mode": "execution", "outputs": outputs}

    next_path = workspace / "docs" / "next.md"
    ensure_dir(next_path.parent)
    next_path.write_text(create_setup_pending_next_markdown(answers, secret_status))
    write_json(runtime_state_path(workspace), create_setup_pending_state(answers, secret_status))
    return {
        "mode": "setup-secrets",
        "outputs": {
            "next": next_path,
            "state": runtime_state_path(workspace),
            "secrets": secrets_status_path(workspace),
        },
        "message": setup_pending_message(secret_status),
    }
