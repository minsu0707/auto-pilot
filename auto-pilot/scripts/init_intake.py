#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from autopilot_lib import format_question, load_or_create_intake_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an Auto Pilot intake session.")
    parser.add_argument("--workspace", default=".", help="Target workspace path.")
    parser.add_argument(
        "--prompt",
        default="",
        help="Initial short project prompt. If provided, question 1 is auto-filled.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    state = load_or_create_intake_state(workspace, args.prompt or None)
    print(format_question(state))


if __name__ == "__main__":
    main()
