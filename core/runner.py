"""Run one shared Phase-3 FSM with OpenVLA or teammate output adapters.

Synchronization boundary
------------------------
* scene/assets/layout/physics and reference cameras: teammate ``with_env_cfg`` release
* spawning and 14-stage semantics: extracted effective teammate contract
* OpenVLA: relative 7D action and 224x224 policy RGB
* teammate: absolute 8D action and original six-camera RGB-D-semantic schema
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import gymnasium as gym
import torch
from pxr import Gf, UsdGeom
import omni.usd

import isaaclab_tasks
import isaaclab.utils.math as math_utils
from isaaclab_tasks.utils import parse_env_cfg

from configs.scene_cfg import configure_phase3_team_env
from core.actions import AbsoluteTeammateActionAdapter, RelativeOpenVLAActionAdapter
from core.contract import (
    CONTRACT_VERSION,
    REQUIRED_ASSETS,
    load_team_workspace,
    resolve_team_env_dir,
    scene_key,
)
from core.fsm import (
    MIN_INTERPOLATION_STEPS,
    Stage,
    StageSpec,
    binary_gripper_command,
    recording_skill,
    stage_specs,
)
from core.object_profiles import (
    ObjectSkillProfile,
    object_profile,
)
from core.spawn import (
    EpisodeSpawn,
    sample_episode_spawn,
)
from recorders.openvla_hdf5_recorder import OpenVLAHDF5Recorder
from recorders.contract import RecorderStep
from recorders.teammate_hdf5_recorder import (
    TeammateHDF5Recorder,
    write_dataset_norm_stats,
)


BASE_GRIP_QUAT = (0.0, 0.7071, 0.7071, 0.0)
SCALPEL_LOCAL_CENTER = (0.0, 0.0656, 0.0)
SETTLE_STEPS = 150
SETTLE_VELOCITY = 0.003
SETTLE_POLL_EVERY = 10
SETTLE_CONSECUTIVE = 3


def _quat_from_rotmat(matrix: torch.Tensor) -> torch.Tensor:
    """Convert a 3x3 rotation matrix to a normalized wxyz quaternion."""

    m = matrix
    trace = m[0, 0] + m[1, 1] + m[2, 2]
    if float(trace) > 0.0:
        scale = torch.sqrt(trace + 1.0) * 2.0
        values = (0.25 * scale, (m[2, 1] - m[1, 2]) / scale,
                  (m[0, 2] - m[2, 0]) / scale, (m[1, 0] - m[0, 1]) / scale)
    elif float(m[0, 0]) > float(m[1, 1]) and float(m[0, 0]) > float(m[2, 2]):
        scale = torch.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        values = ((m[2, 1] - m[1, 2]) / scale, 0.25 * scale,
                  (m[0, 1] + m[1, 0]) / scale, (m[0, 2] + m[2, 0]) / scale)
    elif float(m[1, 1]) > float(m[2, 2]):
        scale = torch.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        values = ((m[0, 2] - m[2, 0]) / scale, (m[0, 1] + m[1, 0]) / scale,
                  0.25 * scale, (m[1, 2] + m[2, 1]) / scale)
    else:
        scale = torch.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        values = ((m[1, 0] - m[0, 1]) / scale, (m[0, 2] + m[2, 0]) / scale,
                  (m[1, 2] + m[2, 1]) / scale, 0.25 * scale)
    quat = torch.stack(tuple(torch.as_tensor(v, device=m.device) for v in values))
    return quat / (torch.linalg.norm(quat) + 1.0e-9)


def _scalpel_quat(yaw_rad: float, pose_mode: str, device: str) -> torch.Tensor:
    yaw = torch.tensor(yaw_rad, device=device)
    cosine, sine = torch.cos(yaw), torch.sin(yaw)
    zero = torch.tensor(0.0, device=device)
    if pose_mode == "EDGE_SIDE":
        world_x = torch.tensor((0.0, 0.0, 1.0), device=device)
        world_y = torch.stack((cosine, sine, zero))
    else:
        world_x = torch.stack((cosine, sine, zero))
        world_y = torch.tensor((0.0, 0.0, -1.0), device=device)
    world_z = torch.cross(world_x, world_y, dim=0)
    matrix = torch.stack((world_x, world_y, world_z), dim=1)
    return _quat_from_rotmat(matrix)


def _yaw_quat(yaw_rad: float, device: str) -> torch.Tensor:
    half = torch.tensor(yaw_rad * 0.5, device=device)
    return torch.stack((torch.cos(half), torch.zeros_like(half), torch.zeros_like(half), torch.sin(half)))


def _spawn_tray(stage, team_dir: Path, tray_xyz: tuple[float, float, float]) -> None:
    path = "/World/RandomTray"
    old = stage.GetPrimAtPath(path)
    if old.IsValid():
        stage.RemovePrim(path)
    tray = UsdGeom.Xform.Define(stage, path)
    tray.GetPrim().GetReferences().AddReference(
        str(team_dir / "assets" / "SurgicalTray.usd"), "/Root/SurgicalTray"
    )
    tray.ClearXformOpOrder()
    tray.AddTranslateOp().Set(Gf.Vec3d(*tray_xyz))
    tray.AddScaleOp().Set(Gf.Vec3d(0.0025, 0.0025, 0.0025))


def _write_spawn(env, spawn: EpisodeSpawn) -> None:
    for item in spawn.objects:
        asset = env.scene[scene_key(item.category, spawn.target)]
        yaw_rad = math.radians(item.yaw_deg)
        if item.category == "scalpel":
            quat = _scalpel_quat(yaw_rad, item.pose_mode or "BROAD_FLAT", env.device)
            center = torch.tensor(item.xyz, device=env.device)
            local_center = torch.tensor(SCALPEL_LOCAL_CENTER, device=env.device)
            root_pos = center - math_utils.quat_apply(quat.unsqueeze(0), local_center.unsqueeze(0))[0]
        else:
            quat = _yaw_quat(yaw_rad, env.device)
            root_pos = torch.tensor(item.xyz, device=env.device)
        pose = torch.zeros((env.num_envs, 7), device=env.device)
        pose[:, :3] = root_pos
        pose[:, 3:] = quat
        asset.write_root_pose_to_sim(pose)
        asset.write_root_velocity_to_sim(torch.zeros((env.num_envs, 6), device=env.device))
        asset.update(dt=env.physics_dt)


def _ee_pose(env) -> tuple[torch.Tensor, torch.Tensor]:
    # Use the exact TCP controlled by DiffIK and by the original Rheo2 expert.
    # Isaac Lift's ee_frame sensor uses 0.1034 m, but the controller body
    # offset is 0.107 m; using the sensor directly leaves the fingers high.
    robot = env.scene["robot"]
    body_ids, _ = robot.find_bodies("panda_hand")
    hand_pos = robot.data.body_pos_w[0, body_ids[0]].clone()
    hand_quat = robot.data.body_quat_w[0, body_ids[0]].clone()
    tcp_offset = torch.tensor((0.0, 0.0, 0.107), device=env.device)
    tcp_pos = hand_pos + math_utils.quat_apply(hand_quat.unsqueeze(0), tcp_offset.unsqueeze(0))[0]
    return tcp_pos, hand_quat


def _object_center(env, target: str) -> torch.Tensor:
    asset = env.scene["object"]
    root = asset.data.root_pos_w[0].clone()
    if target != "scalpel":
        return root
    local = torch.tensor(SCALPEL_LOCAL_CENTER, device=env.device)
    return root + math_utils.quat_apply(asset.data.root_quat_w[0:1], local.unsqueeze(0))[0]


def _wait_for_settle(env, spawn: EpisodeSpawn, action_adapter):
    current_pos, current_quat = _ee_pose(env)
    action = action_adapter.make_action(
        env,
        current_pos,
        current_quat,
        current_pos,
        current_quat,
        1.0,
    )
    obs = None
    consecutive = 0
    categories = [entry.category for entry in spawn.objects]
    for step in range(SETTLE_STEPS + SETTLE_CONSECUTIVE * SETTLE_POLL_EVERY):
        obs, _, _, _, _ = env.step(action)
        if step < SETTLE_STEPS or step % SETTLE_POLL_EVERY:
            continue
        speeds = [
            float(torch.linalg.norm(env.scene[scene_key(name, spawn.target)].data.root_lin_vel_w[0]))
            for name in categories
        ]
        consecutive = consecutive + 1 if max(speeds) < SETTLE_VELOCITY else 0
        if consecutive >= SETTLE_CONSECUTIVE:
            break
    for _ in range(10):
        obs, _, _, _, _ = env.step(action)
    return obs


def _slerp(q0: torch.Tensor, q1: torch.Tensor, fraction: float) -> torch.Tensor:
    first = q0 / (torch.linalg.norm(q0) + 1.0e-9)
    second = q1 / (torch.linalg.norm(q1) + 1.0e-9)
    dot = torch.clamp(torch.dot(first, second), -1.0, 1.0)
    if float(dot) < 0.0:
        second, dot = -second, -dot
    if float(dot) > 0.9995:
        value = first + fraction * (second - first)
        return value / (torch.linalg.norm(value) + 1.0e-9)
    theta = torch.acos(dot)
    return (
        torch.sin((1.0 - fraction) * theta) / torch.sin(theta) * first
        + torch.sin(fraction * theta) / torch.sin(theta) * second
    )


def _grasp_pose(env, profile: ObjectSkillProfile, table_z: float, spawn: EpisodeSpawn):
    asset = env.scene["object"]
    root_pos = asset.data.root_pos_w[0].clone()
    root_quat = asset.data.root_quat_w[0].clone()
    if profile.category == "scalpel":
        center = _object_center(env, profile.category)
        spawn_item = spawn.object("scalpel")
        local_axis = (0.0, 1.0, 0.0) if spawn_item.pose_mode == "EDGE_SIDE" else (1.0, 0.0, 0.0)
        world_axis = math_utils.quat_apply(
            root_quat.unsqueeze(0), torch.tensor(local_axis, device=env.device).unsqueeze(0)
        )[0]
        yaw = torch.atan2(world_axis[1], world_axis[0]) + math.radians(profile.grasp_yaw_offset_deg)
        grasp = center.clone()
        grasp[2] = max(profile.grasp_z_min, table_z + profile.grasp_above_table)
        if profile.grasp_z_max is not None:
            grasp[2] = min(float(grasp[2]), profile.grasp_z_max)
    else:
        root_yaw = math_utils.euler_xyz_from_quat(root_quat.unsqueeze(0))[2][0]
        yaw = root_yaw + math.radians(profile.grasp_yaw_offset_deg)
        planar_offset = math_utils.quat_apply(
            _yaw_quat(float(root_yaw), env.device).unsqueeze(0),
            torch.tensor(profile.body_offset, device=env.device).unsqueeze(0),
        )[0]
        grasp = root_pos + planar_offset
        contact_z = max(table_z + profile.grasp_z_min, float(root_pos[2]) + profile.grasp_above_table)
        grasp[2] = contact_z + profile.body_offset[2] + profile.grasp_z_adjust
    yaw_quaternion = _yaw_quat(float(yaw), env.device)
    grip_quaternion = torch.tensor(BASE_GRIP_QUAT, device=env.device)
    desired_quat = math_utils.quat_mul(yaw_quaternion.unsqueeze(0), grip_quaternion.unsqueeze(0))[0]
    return grasp, desired_quat


def _waypoints(
    env,
    profile: ObjectSkillProfile,
    grasp: torch.Tensor,
    spawn: EpisodeSpawn,
) -> dict[Stage, torch.Tensor]:
    close = grasp.clone()
    close[2] -= profile.lower_extra_z
    tray = torch.tensor(spawn.tray_xyz, device=env.device)
    slot = tray + torch.tensor(profile.tray_slot_offset, device=env.device)
    lower_place = slot + torch.tensor((0.0, 0.0, 0.035), device=env.device)
    return {
        Stage.OPEN_HOVER: grasp + torch.tensor((0.0, 0.0, 0.23), device=env.device),
        Stage.LOWER_PRE: grasp + torch.tensor((0.0, 0.0, 0.060), device=env.device),
        Stage.LOWER_GRASP: grasp,
        Stage.LOWER_EXTRA: close,
        Stage.HOLD_BEFORE_CLOSE: close,
        Stage.CLOSE: close,
        Stage.HOLD_AFTER_CLOSE: close,
        Stage.MICRO_LIFT: close + torch.tensor((0.0, 0.0, profile.micro_lift_height), device=env.device),
        Stage.LIFT_MID: close + torch.tensor((0.0, 0.0, 0.16), device=env.device),
        Stage.LIFT: close + torch.tensor((0.0, 0.0, 0.28), device=env.device),
        Stage.MOVE_PLACE: slot + torch.tensor((0.0, 0.0, 0.18), device=env.device),
        Stage.LOWER_PLACE: lower_place,
        Stage.OPEN: lower_place,
        Stage.RETREAT: slot + torch.tensor((0.0, 0.0, 0.22), device=env.device),
    }


def _run_stage(
    env,
    spec: StageSpec,
    target_pos: torch.Tensor,
    target_quat: torch.Tensor,
    profile: ObjectSkillProfile,
    obs,
    recorders: dict[str, Any],
    action_adapter,
    settings: Any,
):
    start_pos, start_quat = _ee_pose(env)
    settled = 0
    max_object_z = float(env.scene["object"].data.root_pos_w[0, 2])
    for step in range(spec.max_steps):
        fraction = min(1.0, (step + 1) / max(MIN_INTERPOLATION_STEPS, 1))
        desired_pos = start_pos + fraction * (target_pos - start_pos) if spec.mode == "pose" else target_pos
        desired_quat = _slerp(start_quat, target_quat, fraction) if spec.mode == "pose" else target_quat
        grip = binary_gripper_command(spec, step, smooth_close=profile.smooth_close)
        current_pos, current_quat = _ee_pose(env)
        action = action_adapter.make_action(
            env,
            current_pos,
            current_quat,
            desired_pos,
            desired_quat,
            grip,
        )
        skill = recording_skill(spec.stage, settings.include_scripted_stages)
        if skill in recorders:
            recorders[skill].add_step(
                RecorderStep(
                    env=env,
                    observation=obs,
                    action=action,
                    stage_name=spec.stage.value,
                    stage_suffix=spec.stage.value,
                    step_id=step,
                    skill=skill,
                )
            )
        obs, _, _, truncated, _ = env.step(action)
        if bool(truncated.any()):
            raise RuntimeError(f"environment timeout in {spec.stage.value}")

        current_pos, _ = _ee_pose(env)
        distance = float(torch.linalg.norm(current_pos - target_pos))
        max_object_z = max(max_object_z, float(env.scene["object"].data.root_pos_w[0, 2]))
        if step == 0 or (settings.debug_every > 0 and step % settings.debug_every == 0):
            print(f"[{spec.stage.value}] step={step:03d} distance={distance:.4f} grip={grip:+.0f}")
        if spec.mode == "pose" and not spec.force_wait and step + 1 >= MIN_INTERPOLATION_STEPS:
            settled = settled + 1 if distance < spec.distance_threshold else 0
            if settled >= spec.settle_steps:
                break
    return obs, max_object_z


def _segment_dir(root: Path, skill: str, target: str) -> Path:
    path = root / skill / target
    path.mkdir(parents=True, exist_ok=True)
    return path


def _next_episode_id(path: Path) -> int:
    ids = []
    for file in path.glob("episode_*.h5"):
        try:
            ids.append(int(file.stem.rsplit("_", 1)[1]))
        except ValueError:
            pass
    return max(ids, default=-1) + 1


def _save(
    recorder: Any,
    episode_id: int,
    metadata: dict[str, object],
) -> bool:
    return recorder.save_episode(episode_id, metadata) is not None


def _collector_kind(settings: Any) -> str:
    collector = str(getattr(settings, "collector", "openvla"))
    if collector not in {"openvla", "teammate"}:
        raise ValueError(f"Unknown collector: {collector}")
    return collector


def _action_adapter(settings: Any):
    if _collector_kind(settings) == "teammate":
        return AbsoluteTeammateActionAdapter()
    return RelativeOpenVLAActionAdapter(
        kp=settings.kp,
        kp_rot=settings.kp_rot,
        max_delta=settings.max_delta,
        max_rot_delta=settings.max_rot_delta,
    )


def _output_directories(
    output_root: Path,
    wanted: set[str],
    target: str,
    collector: str,
) -> dict[str, Path]:
    names = {
        "pick_lift": "pick_policy" if collector == "teammate" else "pick_lift",
        "place": "place_policy" if collector == "teammate" else "place",
    }
    return {
        skill: _segment_dir(output_root, names[skill], target)
        for skill in wanted
    }


def _make_recorders(
    settings: Any,
    directories: dict[str, Path],
    profile: ObjectSkillProfile,
    spawn: EpisodeSpawn,
    team_dir: Path,
) -> dict[str, Any]:
    recorders = {}
    for skill, path in directories.items():
        instruction = (
            f"Pick up the {profile.display_name}."
            if skill == "pick_lift"
            else f"Place the {profile.display_name} in its tray slot."
        )
        if _collector_kind(settings) == "teammate":
            recorders[skill] = TeammateHDF5Recorder(
                output_dir=path,
                task_description=instruction,
                target=settings.target,
                skill=skill,
                spawn=spawn,
                profile=profile,
                team_env_dir=team_dir,
                debug_every=settings.debug_every,
            )
        else:
            recorders[skill] = OpenVLAHDF5Recorder(
                output_dir=str(path),
                task_description=instruction,
            )
    return recorders


def run_collection(settings: Any, simulation_app: Any) -> None:
    """Run synchronized Phase-3 collection using parsed CLI settings."""

    if settings.episodes < 1:
        raise ValueError("--episodes must be >= 1")
    team_dir = resolve_team_env_dir(settings.phase3_dir)
    workspace = load_team_workspace(team_dir)
    profile = object_profile(settings.target)
    output_root = Path(settings.output_dir).expanduser().resolve()
    collector = _collector_kind(settings)
    action_adapter = _action_adapter(settings)

    env_cfg = parse_env_cfg(settings.task, device=settings.device, num_envs=1)
    env_cfg.seed = settings.seed
    env_cfg.episode_length_s = settings.episode_length_s
    configure_phase3_team_env(
        env_cfg,
        target=settings.target,
        action_mode="absolute" if collector == "teammate" else "relative",
        team_env_dir=team_dir,
    )
    env = gym.make(settings.task, cfg=env_cfg).unwrapped
    stage = omni.usd.get_context().get_stage()
    _spawn_tray(stage, team_dir, workspace.tray_position)

    wanted = {"pick_lift", "place"} if settings.record_skill == "both" else {settings.record_skill}
    directories = _output_directories(output_root, wanted, settings.target, collector)
    next_ids = {skill: _next_episode_id(path) for skill, path in directories.items()}
    if collector == "teammate" and len(next_ids) > 1:
        shared_next_id = max(next_ids.values())
        next_ids = {skill: shared_next_id for skill in next_ids}
    saved = 0
    attempt = 0
    maximum_attempts = settings.max_attempts or settings.episodes * 50

    print(f"[SYNC] contract={CONTRACT_VERSION} collector={collector} target={settings.target}")
    print(f"[SYNC] teammate_env={team_dir}")
    print(f"[SYNC] action={action_adapter.action_type} ({action_adapter.action_dim}D)")
    print(
        "[SYNC] cameras=openvla RGB 224x224 + wrist"
        if collector == "openvla"
        else "[SYNC] cameras=teammate six-view RGB-D-semantic 448x336"
    )
    print(f"[SYNC] assets={len(REQUIRED_ASSETS)} referenced in place")

    try:
        while simulation_app.is_running() and saved < settings.episodes and attempt < maximum_attempts:
            attempt += 1
            env.reset()
            spawn = sample_episode_spawn(workspace, settings.target, attempt, settings.seed)
            _write_spawn(env, spawn)
            obs = _wait_for_settle(env, spawn, action_adapter)

            recorders = _make_recorders(
                settings,
                directories,
                profile,
                spawn,
                team_dir,
            )
            grasp, grasp_quat = _grasp_pose(env, profile, workspace.offset[2], spawn)
            waypoints = _waypoints(env, profile, grasp, spawn)
            initial_z = float(env.scene["object"].data.root_pos_w[0, 2])
            max_z = initial_z
            close_z = initial_z
            pick_ok = False
            place_ok = False
            error = ""

            try:
                for spec in stage_specs(profile):
                    obs, stage_max_z = _run_stage(
                        env,
                        spec,
                        waypoints[spec.stage],
                        grasp_quat,
                        profile,
                        obs,
                        recorders,
                        action_adapter,
                        settings,
                    )
                    max_z = max(max_z, stage_max_z)
                    if spec.stage is Stage.HOLD_AFTER_CLOSE:
                        close_z = float(env.scene["object"].data.root_pos_w[0, 2])
                    elif spec.stage is Stage.MICRO_LIFT:
                        after_micro = float(env.scene["object"].data.root_pos_w[0, 2])
                        if after_micro <= close_z + profile.micro_lift_success_delta:
                            raise RuntimeError(
                                f"micro-lift failed: close_z={close_z:.4f}, after={after_micro:.4f}"
                            )
                    elif spec.stage is Stage.LIFT:
                        pick_ok = max_z > close_z + 0.06
                        if not pick_ok:
                            raise RuntimeError(f"lift gate failed: max_z={max_z:.4f}, close_z={close_z:.4f}")
                        if settings.record_skill == "pick_lift":
                            break

                if pick_ok and settings.record_skill != "pick_lift":
                    final_center = _object_center(env, settings.target)
                    tray = torch.tensor(spawn.tray_xyz, device=env.device)
                    slot = tray + torch.tensor(profile.tray_slot_offset, device=env.device)
                    xy_error = float(torch.linalg.norm((final_center - slot)[:2]))
                    place_ok = xy_error < 0.09 and float(final_center[2]) < 0.12
                    if not place_ok:
                        raise RuntimeError(
                            f"place gate failed: xy_error={xy_error:.4f}, z={float(final_center[2]):.4f}"
                        )
                elif pick_ok:
                    place_ok = True
            except RuntimeError as exception:
                error = str(exception)

            metadata = {
                "contract_version": CONTRACT_VERSION,
                "target_object": settings.target,
                "attempt": attempt,
                "seed": settings.seed,
                "cell_id": spawn.cell_id,
                "grid_row": spawn.row,
                "grid_col": spawn.col,
                "spawn": spawn.as_dict(),
                "action_semantics": action_adapter.action_type,
                "primary_camera": "openvla_camera" if collector == "openvla" else "camera",
                "primary_image_resolution": "224x224" if collector == "openvla" else "448x336",
                "wrist_camera": "grip_cam_b",
                "teammate_env_dir": str(team_dir),
                "shared_fsm": True,
                "shared_spawn": True,
            }
            saved_this_attempt = True
            if collector == "teammate":
                full_success = pick_ok and (
                    settings.record_skill == "pick_lift" or place_ok
                )
                if full_success:
                    for skill, recorder in recorders.items():
                        saved_this_attempt &= _save(recorder, next_ids[skill], metadata)
                        if saved_this_attempt:
                            next_ids[skill] += 1
                else:
                    saved_this_attempt = False
            else:
                if "pick_lift" in recorders:
                    if pick_ok:
                        saved_this_attempt &= _save(
                            recorders["pick_lift"],
                            next_ids["pick_lift"],
                            metadata,
                        )
                        next_ids["pick_lift"] += 1
                    else:
                        saved_this_attempt = False
                if "place" in recorders:
                    if place_ok:
                        saved_this_attempt &= _save(
                            recorders["place"],
                            next_ids["place"],
                            metadata,
                        )
                        next_ids["place"] += 1
                    else:
                        saved_this_attempt = False
            if saved_this_attempt:
                saved += 1
                print(f"[SAVE] synchronized episode {saved}/{settings.episodes}")
            else:
                print(f"[RETRY] attempt={attempt}: {error or 'required segment did not pass'}")

        if collector == "teammate":
            for path in directories.values():
                write_dataset_norm_stats(path)

        if saved < settings.episodes:
            raise RuntimeError(
                f"Saved {saved}/{settings.episodes} episodes after {attempt} attempts"
            )
        print(f"[DONE] saved={saved} output={output_root}")
    finally:
        env.close()
        simulation_app.close()
