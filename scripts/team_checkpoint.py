#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import re
from pathlib import Path

from autopilot_lib import load_json, write_json


ROLE_LABELS = {
    "manager": "Manager",
    "planner": "Planner",
    "architect": "Architect",
    "builder": "Builder",
    "designer": "Designer",
    "qa": "QA",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record Auto Pilot team checkpoint results.")
    parser.add_argument("--workspace", default=".", help="Target workspace path.")
    parser.add_argument("--role", required=True, choices=sorted(ROLE_LABELS.keys()))
    parser.add_argument("--summary", required=True, help="Short summary of the role output.")
    parser.add_argument("--next-owner", help="Next owner role label, for example Builder or QA.")
    parser.add_argument("--next-task", help="Next current task text.")
    parser.add_argument("--planner-checkpoint", help="Planner checkpoint text.")
    parser.add_argument("--planner-intent", help="Planner intent block for docs/next.md.")
    parser.add_argument("--builder-target", help="Builder target block for docs/next.md.")
    parser.add_argument("--architect-guardrails", help="Architect guardrails block for docs/next.md.")
    parser.add_argument("--designer-notes", help="Designer notes block for docs/progress.md or docs/next.md.")
    parser.add_argument("--builder-progress", help="Builder progress block for docs/progress.md.")
    parser.add_argument("--reviewer-verdict", help="Designer or QA verdict text.")
    parser.add_argument("--qa-check", action="append", dest="qa_checks", default=[], help="One QA check line.")
    parser.add_argument("--design-review-note", help="Design review notes to append or replace in docs/design.md.")
    parser.add_argument("--blocker-classification", choices=["retryable", "deferable", "human-required"])
    parser.add_argument("--blocker-summary", help="Short blocker summary to add to active blockers.")
    parser.add_argument("--blocker-owner-role", help="Owner role for the blocker; defaults to the current role.")
    parser.add_argument("--resolve-blocker", action="append", default=[], help="Exact blocker summary to move from active to resolved.")
    return parser.parse_args()


def markdown_block(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if text.startswith("- ") or text.startswith("1. ") or "\n- " in text or "\n1. " in text:
        return text
    return f"- {text}"


def replace_or_insert_section(document: str, heading: str, body: str, after: tuple[str, ...] = ()) -> str:
    body = body.strip()
    replacement = f"## {heading}\n\n{body}\n"
    pattern = rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)"
    if re.search(pattern, document):
        return re.sub(pattern, replacement + "\n", document).rstrip() + "\n"

    for anchor in after:
        anchor_pattern = rf"(?ms)^## {re.escape(anchor)}\n\n.*?(?=^## |\Z)"
        match = re.search(anchor_pattern, document)
        if match:
            insert_at = match.end()
            return document[:insert_at].rstrip() + "\n\n" + replacement + "\n" + document[insert_at:].lstrip()

    return document.rstrip() + "\n\n" + replacement + "\n"


def load_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def save_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def update_progress(progress_path: Path, args: argparse.Namespace) -> None:
    progress = load_text(progress_path)
    if args.role == "planner":
        planner_body = markdown_block(args.planner_checkpoint or args.summary)
        progress = replace_or_insert_section(progress, "Planner Notes", planner_body, after=("Recently Completed",))
    elif args.role == "architect":
        progress = replace_or_insert_section(progress, "Architect Notes", markdown_block(args.summary), after=("Planner Notes",))
    elif args.role == "builder":
        progress = replace_or_insert_section(
            progress,
            "Builder Progress",
            markdown_block(args.builder_progress or args.summary),
            after=("Planner Notes", "Architect Notes"),
        )
    elif args.role == "designer":
        progress = replace_or_insert_section(
            progress,
            "Designer Notes",
            markdown_block(args.designer_notes or args.summary),
            after=("Builder Progress", "Architect Notes"),
        )
    elif args.role == "qa":
        verdict = args.reviewer_verdict or args.summary
        progress = replace_or_insert_section(progress, "QA Verdict", markdown_block(verdict), after=("Designer Notes", "Builder Progress"))
    elif args.role == "manager":
        progress = replace_or_insert_section(progress, "Manager Notes", markdown_block(args.summary), after=("QA Verdict",))
    save_text(progress_path, progress)


def update_next(next_path: Path, args: argparse.Namespace) -> None:
    next_doc = load_text(next_path)
    if args.role == "planner":
        next_doc = replace_or_insert_section(
            next_doc,
            "Planner Intent",
            markdown_block(args.planner_intent or args.planner_checkpoint or args.summary),
            after=("Execution Mode",),
        )
        if args.builder_target:
            next_doc = replace_or_insert_section(next_doc, "Builder Target", markdown_block(args.builder_target), after=("Planner Intent",))
        if args.qa_checks:
            next_doc = replace_or_insert_section(
                next_doc,
                "QA Checks",
                "\n".join(f"- {check.strip()}" for check in args.qa_checks if check.strip()),
                after=("Designer Notes", "Architect Guardrails", "Builder Target"),
            )
    elif args.role == "architect":
        next_doc = replace_or_insert_section(
            next_doc,
            "Architect Guardrails",
            markdown_block(args.architect_guardrails or args.summary),
            after=("Builder Target", "Planner Intent"),
        )
    elif args.role == "designer":
        next_doc = replace_or_insert_section(
            next_doc,
            "Designer Notes",
            markdown_block(args.designer_notes or args.summary),
            after=("Architect Guardrails", "Builder Target"),
        )
    elif args.role == "qa" and args.qa_checks:
        next_doc = replace_or_insert_section(
            next_doc,
            "QA Checks",
            "\n".join(f"- {check.strip()}" for check in args.qa_checks if check.strip()),
            after=("Designer Notes", "Architect Guardrails", "Builder Target"),
        )
    save_text(next_path, next_doc)


def update_design(design_path: Path, args: argparse.Namespace) -> None:
    if not design_path.exists() or not args.design_review_note:
        return
    design = load_text(design_path)
    design = replace_or_insert_section(
        design,
        "Design Review Notes",
        markdown_block(args.design_review_note),
    )
    save_text(design_path, design)


def update_blockers(blockers_path: Path, args: argparse.Namespace) -> None:
    blockers = load_json(blockers_path) if blockers_path.exists() else {"active": [], "resolved": []}
    active = blockers.setdefault("active", [])
    resolved = blockers.setdefault("resolved", [])

    if args.resolve_blocker:
        remaining = []
        targets = set(args.resolve_blocker)
        for item in active:
            if item.get("summary") in targets:
                resolved.append(item)
            else:
                remaining.append(item)
        blockers["active"] = remaining

    if args.blocker_classification and args.blocker_summary:
        active.append(
            {
                "ownerRole": args.blocker_owner_role or ROLE_LABELS[args.role],
                "classification": args.blocker_classification,
                "summary": args.blocker_summary,
                "updatedAt": now_iso(),
            }
        )

    write_json(blockers_path, blockers)


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    state_path = workspace / "autopilot" / "state.json"
    progress_path = workspace / "docs" / "progress.md"
    next_path = workspace / "docs" / "next.md"
    design_path = workspace / "docs" / "design.md"
    blockers_path = workspace / "autopilot" / "blockers.json"

    state = load_json(state_path)
    last_role_results = state.setdefault("lastRoleResults", {})
    last_role_results[args.role] = args.summary.strip()

    if args.role == "planner":
        state["lastPlannerCheckpoint"] = args.planner_checkpoint or args.summary.strip()
    if args.role in {"designer", "qa"}:
        state["lastReviewerVerdict"] = (args.reviewer_verdict or args.summary).strip()

    if args.next_owner:
        state["currentOwner"] = args.next_owner.strip()
    if args.next_task:
        state["currentTask"] = args.next_task.strip()

    write_json(state_path, state)
    update_progress(progress_path, args)
    update_next(next_path, args)
    update_design(design_path, args)
    update_blockers(blockers_path, args)

    print(f"role: {ROLE_LABELS[args.role]}")
    print(f"state: {state_path}")
    print(f"progress: {progress_path}")
    print(f"next: {next_path}")
    if design_path.exists():
        print(f"design: {design_path}")
    print(f"blockers: {blockers_path}")


if __name__ == "__main__":
    main()
