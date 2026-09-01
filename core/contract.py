"""Pure-Python contract for the synchronized Phase-3 data pipeline.

This module deliberately does not import Isaac Lab.  It identifies the teammate
release that owns the assets/layout and exposes the small set of effective
runtime constants consumed by spawning, tests, and the Isaac-facing bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Mapping


CONTRACT_VERSION = "phase3-team-sync-v1"
TEAM_ENV_VARIABLE = "PHASE3_TEAM_ENV_DIR"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEAM_RELEASE_RELATIVE = Path("teammate_env")

ALL_OBJECTS = (
    "scalpel",
    "scissor",
    "love_retractor",
    "kelly",
    "scalpel_type2",
)

REQUIRED_TEAM_FILES = (
    "phase3_shared_env_cfg.py",
    "phase3_camera_tuning.py",
    "phase3_recorder_camera_patch.py",
    "shared_layout.json",
)

REQUIRED_ASSETS = (
    "knife_centered.usd",
    "my_scissor_clean.usd",
    "love_centered_root_at_center.usd",
    "kelly_root_at_center.usd",
    "scalpel_type2_root.usd",
    "SurgicalTray.usd",
)


@dataclass(frozen=True)
class TeamWorkspace:
    """Resolved values from the teammate's checked-in ``shared_layout.json``."""

    robot_pos: tuple[float, float, float]
    robot_rot: tuple[float, float, float, float]
    table_pos: tuple[float, float, float]
    table_rot: tuple[float, float, float, float]
    offset: tuple[float, float, float]
    active_environment: tuple[str, ...]

    @property
    def tray_position(self) -> tuple[float, float, float]:
        dx, dy, dz = self.offset
        return 0.34 + dx, -0.26 + dy, 0.006 + dz

    @property
    def grid_x(self) -> tuple[float, float]:
        return 0.34 + self.offset[0], 0.64 + self.offset[0]

    @property
    def grid_y(self) -> tuple[float, float]:
        return 0.04 + self.offset[1], 0.32 + self.offset[1]


def resolve_team_env_dir(override: str | os.PathLike[str] | None = None) -> Path:
    """Return and validate the teammate ``with_env_cfg`` directory.

    Resolution order is an explicit argument, ``PHASE3_TEAM_ENV_DIR``, then the
    bundled ``teammate_env`` directory.  Keeping one repository-relative asset
    path makes a fresh clone portable between host and container paths.
    """

    explicit = override or os.environ.get(TEAM_ENV_VARIABLE)
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
    else:
        candidate = (PROJECT_ROOT / TEAM_RELEASE_RELATIVE).resolve()

    missing = [name for name in REQUIRED_TEAM_FILES if not (candidate / name).is_file()]
    missing += [
        f"assets/{name}" for name in REQUIRED_ASSETS
        if not (candidate / "assets" / name).is_file()
    ]
    if missing:
        raise FileNotFoundError(
            f"Invalid Phase-3 teammate directory {candidate}; missing: {missing}"
        )
    return candidate


def load_team_workspace(
    team_env_dir: str | os.PathLike[str] | None = None,
) -> TeamWorkspace:
    root = resolve_team_env_dir(team_env_dir)
    payload: Mapping[str, object] = json.loads(
        (root / "shared_layout.json").read_text(encoding="utf-8")
    )
    robot = payload["robot"]
    table = payload["table"]
    if not isinstance(robot, dict) or not isinstance(table, dict):
        raise ValueError("shared_layout.json robot/table entries must be objects")
    return TeamWorkspace(
        robot_pos=tuple(float(v) for v in robot["pos"]),
        robot_rot=tuple(float(v) for v in robot["rot"]),
        table_pos=tuple(float(v) for v in table["pos"]),
        table_rot=tuple(float(v) for v in table["rot"]),
        offset=tuple(float(v) for v in payload.get("workspace_offset", (0, 0, 0))),
        active_environment=tuple(str(v) for v in payload.get("active_environment", ())),
    )


def scene_key(category: str, target: str) -> str:
    """Map an object category to its single runtime scene entity.

    Isaac Lift owns its target as ``scene.object``.  Using this mapping with
    ``use_canonical_target_only=True`` prevents the duplicate target present in
    the legacy recorder's final effective code.
    """

    if category not in ALL_OBJECTS:
        raise ValueError(f"Unknown object category: {category}")
    if target not in ALL_OBJECTS:
        raise ValueError(f"Unknown target category: {target}")
    return "object" if category == target else category
