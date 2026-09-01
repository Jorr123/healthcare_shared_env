"""Deterministic five-object spawn sampler matching the Phase-3 workspace."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import random

from .contract import ALL_OBJECTS, TeamWorkspace
from .object_profiles import object_profile


GRID_COLS = 5
GRID_ROWS = 4
MIN_OBJECT_DISTANCE = 0.105
MIN_TRAY_DISTANCE = 0.15
YAW_RANGE_DEG = (0.0, 360.0)


@dataclass(frozen=True)
class ObjectSpawn:
    category: str
    xyz: tuple[float, float, float]
    yaw_deg: float
    pose_mode: str | None = None


@dataclass(frozen=True)
class EpisodeSpawn:
    target: str
    attempt: int
    cell_id: int
    row: int
    col: int
    tray_xyz: tuple[float, float, float]
    tray_yaw_deg: float
    objects: tuple[ObjectSpawn, ...]

    def object(self, category: str) -> ObjectSpawn:
        return next(item for item in self.objects if item.category == category)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def grid_cell_center(workspace: TeamWorkspace, cell_id: int) -> tuple[float, float, int, int]:
    cell_id %= GRID_COLS * GRID_ROWS
    row, col = divmod(cell_id, GRID_COLS)
    x0, x1 = workspace.grid_x
    y0, y1 = workspace.grid_y
    x = x0 + (col + 0.5) * (x1 - x0) / GRID_COLS
    y = y0 + (row + 0.5) * (y1 - y0) / GRID_ROWS
    return x, y, row, col


def _range_for(category: str, workspace: TeamWorkspace) -> tuple[tuple[float, float], tuple[float, float]]:
    dx, dy, _ = workspace.offset
    if category == "scalpel":
        return (0.48 + dx, 0.64 + dx), (0.08 + dy, 0.32 + dy)
    if category == "scissor":
        return (0.34 + dx, 0.50 + dx), (0.04 + dy, 0.28 + dy)
    # The final teammate runtime samples Love, Kelly, and type-2 scalpel over
    # the full object grid.  This also fixes a dead constant in the legacy
    # type-2 path that accidentally fell back to the scissor range.
    return workspace.grid_x, workspace.grid_y


def _far_enough(
    xy: tuple[float, float],
    accepted: list[tuple[float, float]],
    tray_xy: tuple[float, float],
) -> bool:
    return all(math.dist(xy, other) >= MIN_OBJECT_DISTANCE for other in accepted) and (
        math.dist(xy, tray_xy) >= MIN_TRAY_DISTANCE
    )


def sample_episode_spawn(
    workspace: TeamWorkspace,
    target: str,
    attempt: int,
    seed: int,
    *,
    max_tries: int = 5000,
) -> EpisodeSpawn:
    """Place the selected target on the 5x4 grid and all four distractors safely."""

    if target not in ALL_OBJECTS:
        raise ValueError(f"Unknown target object: {target}")
    if attempt < 1:
        raise ValueError("attempt must be >= 1")

    rng = random.Random((int(seed) << 32) ^ int(attempt))
    cell_id = (attempt - 1) % (GRID_COLS * GRID_ROWS)
    target_x, target_y, row, col = grid_cell_center(workspace, cell_id)
    tray_xy = workspace.tray_position[:2]

    for _ in range(max_tries):
        positions: dict[str, tuple[float, float]] = {target: (target_x, target_y)}
        accepted = [(target_x, target_y)]
        valid = _far_enough(accepted[0], [], tray_xy)
        for category in ALL_OBJECTS:
            if category == target:
                continue
            xr, yr = _range_for(category, workspace)
            placed = False
            for _candidate_try in range(300):
                xy = (rng.uniform(*xr), rng.uniform(*yr))
                if _far_enough(xy, accepted, tray_xy):
                    positions[category] = xy
                    accepted.append(xy)
                    placed = True
                    break
            if not placed:
                valid = False
                break
        if valid and len(positions) == len(ALL_OBJECTS):
            break
    else:
        raise RuntimeError(
            f"Could not sample a valid five-object layout after {max_tries} tries "
            f"(target={target}, cell={cell_id})"
        )

    objects = []
    for category in ALL_OBJECTS:
        x, y = positions[category]
        profile = object_profile(category)
        mode = None
        z = profile.spawn_root_z + workspace.offset[2]
        if category == "scalpel":
            mode = "BROAD_FLAT" if attempt % 2 == 1 else "EDGE_SIDE"
            z = (0.0008 if mode == "BROAD_FLAT" else 0.0038) + workspace.offset[2]
        objects.append(
            ObjectSpawn(
                category=category,
                xyz=(x, y, z),
                yaw_deg=rng.uniform(*YAW_RANGE_DEG),
                pose_mode=mode,
            )
        )

    return EpisodeSpawn(
        target=target,
        attempt=attempt,
        cell_id=cell_id,
        row=row,
        col=col,
        tray_xyz=workspace.tray_position,
        # This is the teammate recorder's effective runtime transform.  Its
        # declared 90-degree tray constant is never applied by spawn_tray().
        tray_yaw_deg=0.0,
        objects=tuple(objects),
    )


def minimum_pair_distance(spawn: EpisodeSpawn) -> float:
    points = [item.xyz[:2] for item in spawn.objects]
    return min(
        math.dist(points[i], points[j])
        for i in range(len(points))
        for j in range(i + 1, len(points))
    )
