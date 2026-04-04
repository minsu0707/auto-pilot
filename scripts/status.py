#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from autopilot_lib import intake_state_path, load_json, secrets_status_path


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
            return

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
        return

    print("mode: idle")
    print("status: no intake or runtime state found")


if __name__ == "__main__":
    main()
