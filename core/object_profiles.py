"""Per-object parameters for one shared Phase-3 pick/place FSM."""

from __future__ import annotations

from dataclasses import dataclass

from .contract import ALL_OBJECTS


@dataclass(frozen=True)
class ObjectSkillProfile:
    category: str
    display_name: str
    spawn_root_z: float
    body_offset: tuple[float, float, float]
    local_center: tuple[float, float, float]
    grasp_above_table: float
    grasp_z_min: float = 0.003
    grasp_z_max: float | None = None
    grasp_z_adjust: float = 0.0
    lower_extra_z: float = 0.0
    grasp_yaw_offset_deg: float = 0.0
    tray_slot_offset: tuple[float, float, float] = (0.0, 0.055, 0.025)
    hold_before_close_steps: int = 20
    close_steps: int = 100
    hold_after_close_steps: int = 70
    smooth_close: bool = False
    micro_lift_height: float = 0.070
    micro_lift_steps: int = 95
    micro_lift_force_wait: bool = True
    micro_lift_success_delta: float = 0.006
    force_grasp_wait: bool = False


OBJECT_PROFILES = {
    "scalpel": ObjectSkillProfile(
        category="scalpel",
        display_name="scalpel",
        spawn_root_z=0.0008,
        body_offset=(0.0, 0.0, 0.0),
        local_center=(0.0, 0.0656, 0.0),
        grasp_above_table=0.007,
        grasp_z_min=0.004,
        grasp_z_max=0.015,
        lower_extra_z=0.004,
        tray_slot_offset=(0.0, -0.055, 0.025),
        hold_before_close_steps=30,
        close_steps=60,
        hold_after_close_steps=20,
        smooth_close=True,
        micro_lift_height=0.055,
        micro_lift_steps=55,
        micro_lift_force_wait=False,
        micro_lift_success_delta=0.008,
        force_grasp_wait=True,
    ),
    "scissor": ObjectSkillProfile(
        category="scissor",
        display_name="scissor",
        spawn_root_z=0.0025,
        body_offset=(0.0, 0.0, -0.008),
        local_center=(0.0, 0.0, 0.0),
        grasp_above_table=0.005,
    ),
    "love_retractor": ObjectSkillProfile(
        category="love_retractor",
        display_name="Love retractor",
        spawn_root_z=0.001,
        body_offset=(0.0, 0.0, -0.002),
        local_center=(0.0, 0.0, 0.0),
        grasp_above_table=0.005,
        grasp_yaw_offset_deg=90.0,
    ),
    "kelly": ObjectSkillProfile(
        category="kelly",
        display_name="Kelly clamp",
        spawn_root_z=0.014,
        body_offset=(0.0, 0.0, 0.004),
        local_center=(0.0, 0.0, 0.0),
        grasp_above_table=0.018,
        # The Kelly recorder applies its 14 mm correction directly to the
        # LOWER_GRASP waypoint; it does not execute a LOWER_EXTRA stage.
        grasp_z_adjust=-0.014,
    ),
    "scalpel_type2": ObjectSkillProfile(
        category="scalpel_type2",
        display_name="type-2 scalpel",
        spawn_root_z=0.012,
        body_offset=(0.0, 0.0, 0.0),
        local_center=(0.0, 0.0, 0.0),
        grasp_above_table=0.005,
        grasp_yaw_offset_deg=90.0,
    ),
}

assert tuple(OBJECT_PROFILES) == ALL_OBJECTS


def object_profile(category: str) -> ObjectSkillProfile:
    try:
        return OBJECT_PROFILES[category]
    except KeyError as error:
        raise ValueError(f"Unknown object category: {category}") from error
