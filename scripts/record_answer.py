#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from autopilot_lib import (
    format_question,
    intake_state_path,
    load_json,
    prepare_workspace_after_intake,
    record_answer,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record an Auto Pilot intake answer.")
    parser.add_argument("--workspace", default=".", help="Target workspace path.")
    parser.add_argument("--answer", required=True, help="Answer text for the current question.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    try:
        state = record_answer(workspace, args.answer)
    except FileNotFoundError as exc:
        raise SystemExit(str(exc))

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
            return

        print("setup-secrets")
        print(f"next: {outputs['next']}")
        print(f"state: {outputs['state']}")
        print(f"blockers: {outputs['blockers']}")
        print(f"secrets: {outputs['secrets']}")
        print(f"summary: {outputs['summary']}")
        print("")
        print(result["message"])
        return

    print(format_question(load_json(intake_state_path(workspace))))


if __name__ == "__main__":
    main()
