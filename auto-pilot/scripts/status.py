#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from autopilot_lib import intake_state_path, load_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show current Auto Pilot status.")
    parser.add_argument("--workspace", default=".", help="Target workspace path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()

    intake_path = intake_state_path(workspace)
    runtime_path = workspace / "autopilot" / "state.json"
    blockers_path = workspace / "autopilot" / "blockers.json"

    if intake_path.exists():
        intake = load_json(intake_path)
        if intake.get("completed") and runtime_path.exists():
            intake_path.unlink()
        else:
            current_index = intake.get("currentIndex", 1)
            print("mode: intake")
            print(f"current_question_index: {current_index}")
            print(f"completed: {intake.get('completed', False)}")
            return

    if runtime_path.exists():
        state = load_json(runtime_path)
        blockers = load_json(blockers_path) if blockers_path.exists() else {"active": []}
        print("mode: execution")
        print(f"project: {state.get('projectName', '')}")
        print(f"status: {state.get('status', '')}")
        print(f"milestone: {state.get('currentMilestone', '')}")
        print(f"task: {state.get('currentTask', '')}")
        print(f"active_blockers: {len(blockers.get('active', []))}")
        return

    print("mode: idle")
    print("status: no intake or runtime state found")


if __name__ == "__main__":
    main()
