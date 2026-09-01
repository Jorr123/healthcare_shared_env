#!/usr/bin/env python3
"""Collect segmented OpenVLA demonstrations with the shared Phase-3 stack."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from isaaclab.app import AppLauncher


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronized Phase-3 OpenVLA collector")
    parser.add_argument("--task", default="Isaac-Lift-Cube-Franka-IK-Rel-v0")
    parser.add_argument(
        "--target",
        choices=["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"],
        default="scalpel",
    )
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output-dir", default="datasets/rheo2_phase3_synced")
    parser.add_argument("--episode-length-s", type=float, default=25.0)
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=0,
        help="0 allows 50 attempts per requested episode.",
    )
    parser.add_argument("--record-skill", choices=["pick_lift", "place", "both"], default="both")
    parser.add_argument(
        "--include-scripted-stages",
        action="store_true",
        help="Also record OPEN_HOVER and MOVE_PLACE.",
    )
    parser.add_argument(
        "--phase3-dir",
        default=None,
        help="Optional teammate_env path; the bundled directory is used by default.",
    )
    parser.add_argument("--kp", type=float, default=1.0)
    parser.add_argument("--kp-rot", type=float, default=3.1)
    parser.add_argument("--max-delta", type=float, default=0.06)
    parser.add_argument("--max-rot-delta", type=float, default=0.20)
    parser.add_argument("--debug-every", type=int, default=25)
    AppLauncher.add_app_launcher_args(parser)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.collector = "openvla"
    args.enable_cameras = True
    app_launcher = AppLauncher(args)
    simulation_app = app_launcher.app

    # Isaac/Omniverse modules must only be imported after AppLauncher starts.
    from core.runner import run_collection

    run_collection(args, simulation_app)


if __name__ == "__main__":
    main()
