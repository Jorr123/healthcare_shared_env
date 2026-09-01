"""Isaac-facing bridge for the shared scene and both action contracts."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys

import torch

import isaaclab.envs.mdp as mdp
import isaaclab.utils.math as math_utils
from isaaclab.envs import ManagerBasedRLEnv
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

from configs.camera_cfg import (
    OPENVLA_CAMERA_NAME,
    openvla_camera_cfg,
)
from core.contract import ALL_OBJECTS, resolve_team_env_dir


def openvla_proprio_obs(env: ManagerBasedRLEnv, asset_cfg: SceneEntityCfg):
    """Return ``XYZ + RPY + gripper width``, matching the existing Rheo2 data."""

    robot = env.scene[asset_cfg.name]
    hand_pose = robot.data.body_pose_w[:, asset_cfg.body_ids[0]]
    roll, pitch, yaw = math_utils.euler_xyz_from_quat(hand_pose[:, 3:7])
    width = robot.data.joint_pos[:, -2:].sum(dim=1, keepdim=True)
    return torch.cat(
        (
            hand_pose[:, :3],
            roll.unsqueeze(1),
            pitch.unsqueeze(1),
            yaw.unsqueeze(1),
            width,
        ),
        dim=-1,
    )


@configclass
class OpenVLAObservationsCfg:
    @configclass
    class PolicyCfg(ObsGroup):
        image = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg(OPENVLA_CAMERA_NAME),
                "data_type": "rgb",
                "normalize": False,
            },
        )
        wrist_image = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg("grip_cam_b"),
                "data_type": "rgb",
                "normalize": False,
            },
        )
        proprio = ObsTerm(
            func=openvla_proprio_obs,
            params={"asset_cfg": SceneEntityCfg("robot", body_names="panda_hand")},
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = False

    policy: PolicyCfg = PolicyCfg()


def configure_phase3_team_env(
    env_cfg,
    *,
    target: str,
    action_mode: str,
    team_env_dir: str | Path | None = None,
):
    """Apply the shared scene with a relative or absolute DiffIK controller.

    The caller must invoke this after ``AppLauncher`` and before ``gym.make``.
    """

    if target not in ALL_OBJECTS:
        raise ValueError(f"Unknown target category: {target}")
    if action_mode not in {"relative", "absolute"}:
        raise ValueError(f"Unknown action mode: {action_mode}")
    team_dir = resolve_team_env_dir(team_env_dir)
    team_dir_text = str(team_dir)
    if team_dir_text not in sys.path:
        sys.path.insert(0, team_dir_text)

    shared = importlib.import_module("phase3_shared_env_cfg")
    camera_patch = importlib.import_module("phase3_recorder_camera_patch")
    tuning = camera_patch.phase3_load_camera_tuning()
    cameras = tuning.PHASE3_CAMERAS
    grip = cameras["grip_cam_b"]

    request = shared.RecorderEnvRequest(
        target=target,
        distractors=tuple(name for name in ALL_OBJECTS if name != target),
        environment=None,
        # Build the named target once so we can preserve the exact physics used
        # by the teammate recorder, then consolidate it into scene.object.
        use_canonical_target_only=False,
    )
    shared.apply_shared_env_cfg(
        env_cfg,
        request,
        camera_width=int(tuning.CAMERA_WIDTH),
        camera_height=int(tuning.CAMERA_HEIGHT),
        grip_camera_prim=grip["prim_path"],
        grip_pos=tuple(grip["pos"]),
        grip_rot=tuple(grip["rot"]),
    )
    # The legacy scalpel recorder manipulates its named ``scene.scalpel`` copy,
    # whose damping/contact/mass differ from the unused canonical target.  Keep
    # those effective target physics but expose exactly one object under the
    # Lift task's required ``scene.object`` key.
    named_target = getattr(env_cfg.scene, target)
    env_cfg.scene.object = named_target.replace(prim_path="{ENV_REGEX_NS}/Object")
    setattr(env_cfg.scene, target, None)
    camera_patch.phase3_apply_final_cameras_to_env_cfg(env_cfg)
    # Preserve all teammate cameras exactly as configured and add a separate
    # OpenVLA-only RGB view.  The shared workspace translation is applied to
    # both its eye and look-at point.
    env_cfg.scene.openvla_camera = openvla_camera_cfg(shared.WORKSPACE.offset)

    # Both workflows consume the same desired FSM poses. Only the controller
    # representation and recorder schema differ between collectors.
    arm = env_cfg.actions.arm_action
    arm.controller.use_relative_mode = action_mode == "relative"
    arm.scale = 1.0
    env_cfg.observations = OpenVLAObservationsCfg()
    env_cfg.scene.num_envs = 1

    if hasattr(env_cfg, "commands") and hasattr(env_cfg.commands, "object_pose"):
        env_cfg.commands.object_pose.debug_vis = False
    return env_cfg


def configure_phase3_team_openvla_env(
    env_cfg,
    *,
    target: str,
    team_env_dir: str | Path | None = None,
):
    """Backward-compatible wrapper for the relative OpenVLA configuration."""

    return configure_phase3_team_env(
        env_cfg,
        target=target,
        action_mode="relative",
        team_env_dir=team_env_dir,
    )
