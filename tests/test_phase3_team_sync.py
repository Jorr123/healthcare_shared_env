"""Fast tests for the simulator-independent Phase-3 synchronization contract."""

from __future__ import annotations

from core.contract import (
    ALL_OBJECTS,
    REQUIRED_ASSETS,
    load_team_workspace,
    resolve_team_env_dir,
    scene_key,
)
from core.fsm import (
    ORDER,
    Stage,
    binary_gripper_command,
    recording_skill,
    stage_specs,
)
from core.object_profiles import object_profile
from core.spawn import (
    MIN_OBJECT_DISTANCE,
    grid_cell_center,
    minimum_pair_distance,
    sample_episode_spawn,
)


def test_teammate_release_and_assets_resolve():
    team_dir = resolve_team_env_dir()
    assert team_dir.name == "teammate_env"
    assert all((team_dir / "assets" / filename).is_file() for filename in REQUIRED_ASSETS)


def test_one_canonical_target_mapping():
    for target in ALL_OBJECTS:
        keys = [scene_key(category, target) for category in ALL_OBJECTS]
        assert keys.count("object") == 1
        assert len(set(keys)) == len(ALL_OBJECTS)


def test_target_cycles_over_all_grid_cells():
    workspace = load_team_workspace()
    seen = set()
    for attempt in range(1, 21):
        spawn = sample_episode_spawn(workspace, "scalpel", attempt, seed=5)
        seen.add((spawn.row, spawn.col))
        x, y, _, _ = grid_cell_center(workspace, spawn.cell_id)
        assert spawn.object("scalpel").xyz[:2] == (x, y)
    assert len(seen) == 20


def test_every_target_gets_five_spaced_objects():
    workspace = load_team_workspace()
    for target in ALL_OBJECTS:
        for attempt in (1, 7, 20):
            spawn = sample_episode_spawn(workspace, target, attempt, seed=17)
            assert tuple(item.category for item in spawn.objects) == ALL_OBJECTS
            assert minimum_pair_distance(spawn) >= MIN_OBJECT_DISTANCE
            assert spawn.tray_yaw_deg == 0.0


def test_shared_fsm_and_object_specific_optional_stage():
    scalpel_stages = tuple(spec.stage for spec in stage_specs(object_profile("scalpel")))
    assert scalpel_stages == ORDER
    for target in ALL_OBJECTS[1:]:
        stages = tuple(spec.stage for spec in stage_specs(object_profile(target)))
        assert Stage.LOWER_EXTRA not in stages
        assert len(stages) == len(ORDER) - 1


def test_binary_gripper_and_segment_boundaries():
    profile = object_profile("scalpel")
    specs = {spec.stage: spec for spec in stage_specs(profile)}
    for spec in specs.values():
        assert all(
            binary_gripper_command(spec, step, smooth_close=profile.smooth_close) in (-1.0, 1.0)
            for step in range(spec.max_steps)
        )
    assert recording_skill(Stage.OPEN_HOVER) is None
    assert recording_skill(Stage.LOWER_PRE) == "pick_lift"
    assert recording_skill(Stage.MOVE_PLACE) is None
    assert recording_skill(Stage.LOWER_PLACE) == "place"
    assert recording_skill(Stage.OPEN_HOVER, include_scripted_stages=True) == "pick_lift"
    assert recording_skill(Stage.MOVE_PLACE, include_scripted_stages=True) == "place"
