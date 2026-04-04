#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from autopilot_lib import (
    format_question,
    intake_state_path,
    load_or_create_intake_state,
    load_json,
    prepare_workspace_after_intake,
    record_answer,
    secrets_status_path,
    submit_secrets,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto Pilot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Start a new intake session.")
    start.add_argument("--workspace", default=".", help="Target workspace path.")
    start.add_argument("--prompt", default="", help="Initial short project prompt.")

    answer = subparsers.add_parser("answer", help="Record the current intake answer.")
    answer.add_argument("--workspace", default=".", help="Target workspace path.")
    answer.add_argument("--text", required=True, help="Answer text.")

    secrets = subparsers.add_parser("secrets", help="Record upfront integration secrets.")
    secrets.add_argument("--workspace", default=".", help="Target workspace path.")
    secrets.add_argument("--text", required=True, help="Secret payload as KEY=value lines or JSON.")

    status = subparsers.add_parser("status", help="Show intake or execution status.")
    status.add_argument("--workspace", default=".", help="Target workspace path.")

    return parser


def run_start(workspace: Path, prompt: str) -> int:
    state = load_or_create_intake_state(workspace, prompt or None)
    print(format_question(state))
    return 0


def run_answer(workspace: Path, text: str) -> int:
    try:
        state = record_answer(workspace, text)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if state.get("completed"):
        result = prepare_workspace_after_intake(workspace, state["answers"])
        intake_path = intake_state_path(workspace)
        if intake_path.exists():
            intake_path.unlink()
        outputs = result["outputs"]
        if result["mode"] == "execution":
            print("intake-complete")
            print(f"spec: {outputs['spec']}")
            if outputs["design"].exists():
                print(f"design: {outputs['design']}")
            print(f"progress: {outputs['progress']}")
            print(f"next: {outputs['next']}")
            print(f"state: {outputs['state']}")
            print(f"blockers: {outputs['blockers']}")
            print(f"secrets: {outputs['secrets']}")
            print(f"summary: {outputs['summary']}")
            return 0

        print("setup-secrets")
        print(f"next: {outputs['next']}")
        print(f"state: {outputs['state']}")
        print(f"blockers: {outputs['blockers']}")
        print(f"secrets: {outputs['secrets']}")
        print(f"summary: {outputs['summary']}")
        print("")
        print(result["message"])
        return 0

    print(format_question(load_json(intake_state_path(workspace))))
    return 0


def run_secrets(workspace: Path, text: str) -> int:
    try:
        result = submit_secrets(workspace, text)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    outputs = result["outputs"]
    if result["mode"] == "execution":
        print("setup-complete")
        print(f"spec: {outputs['spec']}")
        if outputs["design"].exists():
            print(f"design: {outputs['design']}")
        print(f"progress: {outputs['progress']}")
        print(f"next: {outputs['next']}")
        print(f"state: {outputs['state']}")
        print(f"blockers: {outputs['blockers']}")
        print(f"secrets: {outputs['secrets']}")
        print(f"summary: {outputs['summary']}")
        return 0

    print("setup-secrets")
    print(f"next: {outputs['next']}")
    print(f"state: {outputs['state']}")
    print(f"secrets: {outputs['secrets']}")
    print("")
    print(result["message"])
    return 0


def run_status(workspace: Path) -> int:
    intake_path = intake_state_path(workspace)
    runtime_path = workspace / "autopilot" / "state.json"
    blockers_path = workspace / "autopilot" / "blockers.json"

    if intake_path.exists():
        intake = load_json(intake_path)
        print("mode: intake")
        print(f"current_question_index: {intake.get('currentIndex', 1)}")
        print(f"completed: {intake.get('completed', False)}")
        return 0

    setup_path = secrets_status_path(workspace)
    if setup_path.exists():
        secret_status = load_json(setup_path)
        if secret_status.get("status") == "pending":
            print("mode: setup-secrets")
            print(f"env_file: {secret_status.get('envFilePath', '')}")
            print(f"required_providers: {', '.join(secret_status.get('requiredProviders', []))}")
            print(f"present_keys: {len(secret_status.get('presentKeys', []))}")
            print(f"missing_keys: {len(secret_status.get('missingKeys', []))}")
            if secret_status.get("missingKeys"):
                print(f"missing_key_names: {', '.join(secret_status.get('missingKeys', []))}")
            return 0

    if runtime_path.exists():
        state = load_json(runtime_path)
        blockers = load_json(blockers_path) if blockers_path.exists() else {"active": []}
        print("mode: execution")
        print(f"project: {state.get('projectName', '')}")
        print(f"status: {state.get('status', '')}")
        print(f"milestone: {state.get('currentMilestone', '')}")
        print(f"task: {state.get('currentTask', '')}")
        print(f"execution_mode: {state.get('executionMode', '')}")
        print(f"current_owner: {state.get('currentOwner', '')}")
        print(f"qa_verdict: {state.get('lastReviewerVerdict', '')}")
        print(f"role_results: {', '.join(sorted(state.get('lastRoleResults', {}).keys()))}")
        print(f"active_blockers: {len(blockers.get('active', []))}")
        print(f"setup_status: {state.get('setupStatus', '')}")
        print(f"required_integrations: {', '.join(state.get('requiredIntegrations', []))}")
        print(f"secrets_ready: {state.get('secretsReady', False)}")
        return 0

    print("mode: idle")
    print("status: no intake or runtime state found")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    workspace = Path(getattr(args, "workspace", ".")).resolve()

    if args.command == "start":
        return run_start(workspace, args.prompt)
    if args.command == "answer":
        return run_answer(workspace, args.text)
    if args.command == "secrets":
        return run_secrets(workspace, args.text)
    if args.command == "status":
        return run_status(workspace)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
