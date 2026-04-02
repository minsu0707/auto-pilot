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
        return "모든 필수 질문이 끝났습니다."
    remaining = remaining_questions(state, question)
    return f"{question['index']}. {question['label']}\n남은 질문: {remaining}개"


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


def derive_defaults(answers: dict[str, str]) -> dict[str, str]:
    resolved = dict(answers)
    stack_pref = resolved.get("stack_preferences", "").strip()
    if stack_pref in {"", "기본값", "기본값으로", "기본값으로 해줘"}:
        resolved["stack_preferences"] = "Next.js + TypeScript + Tailwind CSS"

    if not resolved.get("deploy_target", "").strip():
        resolved["deploy_target"] = "Vercel"

    if not resolved.get("data_store", "").strip():
        resolved["data_store"] = "Supabase"

    for key in ("auth_mode", "payments_mode", "admin_required"):
        resolved[key] = normalize_bool_like(resolved.get(key, ""))
        if not resolved[key]:
            resolved[key] = "no"

    if not resolved.get("blocker_policy", "").strip():
        resolved["blocker_policy"] = DEFAULT_BLOCKER_POLICY

    return resolved


def bool_label(value: str) -> str:
    normalized = normalize_bool_like(value)
    if normalized == "yes":
        return "필요"
    if normalized == "no":
        return "불필요"
    return value or "미정"


def create_spec_markdown(answers: dict[str, str]) -> str:
    return f"""# 프로젝트 명세

## 제품 요약

{answers['product_summary']}

## 타겟 사용자

{answers['target_user']}

## 핵심 기능

{answers['core_features']}

## 이번 버전 제외 범위

{answers['non_goals']}

## 기술 스택

{answers['stack_preferences']}

## 운영 제약

- 인증: {bool_label(answers['auth_mode'])}
- 결제: {bool_label(answers['payments_mode'])}
- 관리자 기능: {bool_label(answers['admin_required'])}
- 배포 대상: {answers['deploy_target']}
- 데이터 저장소: {answers['data_store']}

## 디자인 방향

{answers['design_direction']}

## blocker 정책

{answers['blocker_policy']}

## 완료 기준

{answers['definition_of_done']}
"""


def create_progress_markdown(answers: dict[str, str]) -> str:
    return f"""# 진행 상황

## 현재 상태

- intake 완료
- 명세 작성 완료
- 자율 실행 준비 완료

## 최근 완료 작업

- 초기 프로젝트 브리프 확정
- Definition of Done 확정
- 상태 파일 초기화

## 메모

- 제품 요약: {answers['product_summary']}
- 타겟 사용자: {answers['target_user']}
"""


def create_next_markdown(answers: dict[str, str]) -> str:
    return f"""# 다음 작업

## 즉시 수행

1. 프로젝트 초기 구조 생성
2. 핵심 기능을 기준으로 MVP 마일스톤 분해
3. 첫 번째 배포 가능 단위 구현

## 유의 사항

- 인증: {bool_label(answers['auth_mode'])}
- 결제: {bool_label(answers['payments_mode'])}
- 관리자 기능: {bool_label(answers['admin_required'])}
- blocker 정책: {answers['blocker_policy']}

## 완료 기준 참조

{answers['definition_of_done']}
"""


def create_runtime_state(answers: dict[str, str]) -> dict[str, Any]:
    return {
        "projectName": answers["product_summary"],
        "status": "running",
        "currentMilestone": "Project bootstrap",
        "currentTask": "Set up the initial workspace and first implementation slice",
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
