"""Shared logical FSM used by every synchronized Phase-3 object profile.

The teammate release implements these stages as repeated procedural calls.
Here they are explicit and testable.  Object files differ only through
``ObjectSkillProfile`` values, while the stage order stays shared.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .object_profiles import ObjectSkillProfile


class Stage(str, Enum):
    OPEN_HOVER = "OPEN_HOVER"
    LOWER_PRE = "LOWER_PRE"
    LOWER_GRASP = "LOWER_GRASP"
    LOWER_EXTRA = "LOWER_EXTRA"
    HOLD_BEFORE_CLOSE = "HOLD_BEFORE_CLOSE"
    CLOSE = "CLOSE"
    HOLD_AFTER_CLOSE = "HOLD_AFTER_CLOSE"
    MICRO_LIFT = "MICRO_LIFT"
    LIFT_MID = "LIFT_MID"
    LIFT = "LIFT"
    MOVE_PLACE = "MOVE_PLACE"
    LOWER_PLACE = "LOWER_PLACE"
    OPEN = "OPEN"
    RETREAT = "RETREAT"


@dataclass(frozen=True)
class StageSpec:
    stage: Stage
    mode: str
    max_steps: int
    distance_threshold: float = 0.0
    settle_steps: int = 0
    force_wait: bool = False


POSE_SPECS = {
    Stage.OPEN_HOVER: StageSpec(Stage.OPEN_HOVER, "pose", 80, 0.025, 4),
    Stage.LOWER_PRE: StageSpec(Stage.LOWER_PRE, "pose", 80, 0.020, 4),
    Stage.LOWER_GRASP: StageSpec(Stage.LOWER_GRASP, "pose", 120, 0.008, 8),
    Stage.LOWER_EXTRA: StageSpec(Stage.LOWER_EXTRA, "pose", 50, 0.006, 8, True),
    Stage.MICRO_LIFT: StageSpec(Stage.MICRO_LIFT, "pose", 55, 0.020, 8),
    Stage.LIFT_MID: StageSpec(Stage.LIFT_MID, "pose", 70, 0.030, 6),
    Stage.LIFT: StageSpec(Stage.LIFT, "pose", 90, 0.035, 6),
    Stage.MOVE_PLACE: StageSpec(Stage.MOVE_PLACE, "pose", 120, 0.050, 4),
    Stage.LOWER_PLACE: StageSpec(Stage.LOWER_PLACE, "pose", 80, 0.025, 4),
    Stage.RETREAT: StageSpec(Stage.RETREAT, "pose", 80, 0.030, 4),
}

ORDER = (
    Stage.OPEN_HOVER,
    Stage.LOWER_PRE,
    Stage.LOWER_GRASP,
    Stage.LOWER_EXTRA,
    Stage.HOLD_BEFORE_CLOSE,
    Stage.CLOSE,
    Stage.HOLD_AFTER_CLOSE,
    Stage.MICRO_LIFT,
    Stage.LIFT_MID,
    Stage.LIFT,
    Stage.MOVE_PLACE,
    Stage.LOWER_PLACE,
    Stage.OPEN,
    Stage.RETREAT,
)

MIN_INTERPOLATION_STEPS = 12


def stage_specs(profile: ObjectSkillProfile) -> tuple[StageSpec, ...]:
    """Materialize the common sequence with an object's timing parameters."""

    specs: list[StageSpec] = []
    for stage in ORDER:
        if stage is Stage.LOWER_EXTRA and profile.lower_extra_z <= 0.0:
            continue
        if stage is Stage.HOLD_BEFORE_CLOSE:
            spec = StageSpec(stage, "hold", profile.hold_before_close_steps)
        elif stage is Stage.CLOSE:
            spec = StageSpec(stage, "close", profile.close_steps)
        elif stage is Stage.HOLD_AFTER_CLOSE:
            spec = StageSpec(stage, "hold", profile.hold_after_close_steps)
        elif stage is Stage.OPEN:
            spec = StageSpec(stage, "open", 35)
        elif stage is Stage.MICRO_LIFT:
            base = POSE_SPECS[stage]
            spec = StageSpec(
                stage,
                base.mode,
                profile.micro_lift_steps,
                base.distance_threshold,
                base.settle_steps,
                profile.micro_lift_force_wait,
            )
        elif stage is Stage.LOWER_GRASP:
            base = POSE_SPECS[stage]
            spec = StageSpec(
                stage,
                base.mode,
                base.max_steps,
                base.distance_threshold,
                base.settle_steps,
                profile.force_grasp_wait,
            )
        else:
            spec = POSE_SPECS[stage]
        specs.append(spec)
    return tuple(specs)


def recording_skill(stage: Stage, include_scripted_stages: bool = False) -> str | None:
    """Return the user's segmented OpenVLA stream for a stage.

    Approach and transport execute in simulation but remain outside the dataset
    by default, matching the original Rheo2 segmentation philosophy.
    """

    pick = {
        Stage.LOWER_PRE,
        Stage.LOWER_GRASP,
        Stage.LOWER_EXTRA,
        Stage.HOLD_BEFORE_CLOSE,
        Stage.CLOSE,
        Stage.HOLD_AFTER_CLOSE,
        Stage.MICRO_LIFT,
        Stage.LIFT_MID,
        Stage.LIFT,
    }
    place = {Stage.LOWER_PLACE, Stage.OPEN, Stage.RETREAT}
    if include_scripted_stages:
        pick.add(Stage.OPEN_HOVER)
        place.add(Stage.MOVE_PLACE)
    if stage in pick:
        return "pick_lift"
    if stage in place:
        return "place"
    return None


def binary_gripper_command(
    spec: StageSpec,
    step: int,
    *,
    smooth_close: bool,
) -> float:
    """Map teammate grip timing to the Rheo2 binary ``+1/-1`` contract."""

    if spec.mode in {"pose", "hold"}:
        return -1.0 if spec.stage in {
            Stage.HOLD_AFTER_CLOSE,
            Stage.MICRO_LIFT,
            Stage.LIFT_MID,
            Stage.LIFT,
            Stage.MOVE_PLACE,
            Stage.LOWER_PLACE,
        } else 1.0
    if spec.mode == "close":
        if not smooth_close:
            return -1.0
        # The teammate's smooth ramp holds open for 25% then crosses zero
        # halfway through the remaining ramp: 0.25 + 0.75/2 = 0.625.
        return -1.0 if (step + 1) / max(spec.max_steps, 1) >= 0.625 else 1.0
    if spec.mode == "open":
        return 1.0 if (step + 1) / max(spec.max_steps, 1) >= 0.625 else -1.0
    raise ValueError(f"Unknown FSM mode: {spec.mode}")
