#!/usr/bin/env python3
"""Collect teammate-format data with the shared spawn, FSM, and runner."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from isaaclab.app import AppLauncher


TARGETS = ("scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Shared-FSM Phase-3 collector with teammate-compatible HDF5 output."
    )
    # Keep the old positional style while also supporting the team's common
    # --target style.
    parser.add_argument("target_positional", nargs="?", choices=TARGETS)
    parser.add_argument("--target", dest="target_option", choices=TARGETS)
    parser.add_argument("--task", default="Isaac-Lift-Cube-Franka-IK-Abs-v0")
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--output-dir",
        "--out_dir",
        dest="output_dir",
        default="datasets/phase3_shared_teammate",
    )
    parser.add_argument("--episode-length-s", type=float, default=25.0)
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=0,
        help="0 allows 50 attempts per requested episode.",
    )
    parser.add_argument(
        "--record-mode",
        "--record_mode",
        dest="record_mode",
        choices=("pick", "place", "both"),
        default="both",
    )
    parser.add_argument(
        "--phase3-dir",
        default=None,
        help="Optional teammate_env path; the bundled directory is used by default.",
    )
    parser.add_argument("--debug-every", "--debug_every", dest="debug_every", type=int, default=25)
    AppLauncher.add_app_launcher_args(parser)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.target_option and args.target_positional and args.target_option != args.target_positional:
        raise ValueError("Positional target and --target must match when both are provided")
    args.target = args.target_option or args.target_positional or "scalpel"
    args.record_skill = {
        "pick": "pick_lift",
        "place": "place",
        "both": "both",
    }[args.record_mode]
    args.collector = "teammate"
    # The original teammate split schema includes OPEN_HOVER in pick and
    # MOVE_PLACE in place. The shared FSM still owns those stages.
    args.include_scripted_stages = True
    args.enable_cameras = True

    app_launcher = AppLauncher(args)
    simulation_app = app_launcher.app

    # Isaac/Omniverse modules must only be imported after AppLauncher starts.
    from core.runner import run_collection

    run_collection(args, simulation_app)


if __name__ == "__main__":
    main()
