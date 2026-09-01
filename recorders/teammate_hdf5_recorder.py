"""Teammate-compatible multi-camera HDF5 output for the shared FSM."""

from __future__ import annotations

from datetime import datetime
import importlib.util
import json
from pathlib import Path
import re
from typing import Any

import h5py
import numpy as np
import torch

import isaaclab.utils.math as math_utils

from core.contract import resolve_team_env_dir, scene_key
from core.object_profiles import ObjectSkillProfile
from core.spawn import EpisodeSpawn
from recorders.contract import RecorderStep
from recorders.hdf5_validation import validate_teammate_episode


OBJECT_TYPE_IDS = {
    "scalpel": 0,
    "scissor": 1,
    "love_retractor": 2,
    "kelly": 3,
    "scalpel_type2": 4,
}
SKILL_TYPE_IDS = {"pick": 0, "place": 1}
STAGE_TYPE_IDS = {
    "OPEN_HOVER": 0,
    "LOWER_PRE": 1,
    "LOWER_GRASP": 2,
    "LOWER_EXTRA": 3,
    "HOLD_BEFORE_CLOSE": 4,
    "CLOSE": 5,
    "HOLD_AFTER_CLOSE": 6,
    "MICRO_LIFT": 7,
    "LIFT_MID": 8,
    "LIFT": 9,
    "MOVE_PLACE": 10,
    "LOWER_PLACE": 11,
    "OPEN": 12,
    "RETREAT": 13,
}

REALCOMPAT_STATE_KEYS = [
    "joint_pos_0", "joint_pos_1", "joint_pos_2", "joint_pos_3",
    "joint_pos_4", "joint_pos_5", "joint_pos_6",
    "finger_pos_0", "finger_pos_1",
    "ee_pos_bx", "ee_pos_by", "ee_pos_bz",
    "ee_quat_bw", "ee_quat_bx", "ee_quat_by", "ee_quat_bz",
    "object_type_id", "skill_id",
]
ACTION_KEYS = ["x_b", "y_b", "z_b", "qw_b", "qx_b", "qy_b", "qz_b", "gripper"]

SEMANTIC_CLASS_IDS = {
    "background": 0,
    "robot": 1,
    "surgical_tray": 2,
    "scalpel": 3,
    "scissor": 4,
    "love_retractor": 5,
    "kelly": 6,
    "scalpel_type2": 7,
}

CAMERA_VIEWS = ("front", "grip_b", "cam_top", "cam_left", "cam_right", "cam_tray")
VIEW_TO_SCENE_KEY = {
    "front": "camera",
    "grip_b": "grip_cam_b",
    "cam_top": "cam_top",
    "cam_left": "cam_left",
    "cam_right": "cam_right",
    "cam_tray": "cam_tray",
}

STAGE_PREFIX = {
    "scalpel": "SCALPEL",
    "scissor": "SCISSOR",
    "love_retractor": "LOVE",
    "kelly": "KELLY",
    "scalpel_type2": "SCALPEL_TYPE2",
}


def _camera_tuning(team_env_dir: Path):
    path = team_env_dir / "phase3_camera_tuning.py"
    spec = importlib.util.spec_from_file_location("phase3_team_camera_tuning", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load teammate camera tuning: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _numpy(value: Any) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().numpy()
    return np.asarray(value)


def _rgb_uint8(value: Any) -> np.ndarray:
    array = _numpy(value)
    if array.ndim == 4:
        array = array[0]
    if array.shape[-1] == 4:
        array = array[..., :3]
    if array.dtype != np.uint8:
        scale = 255.0 if array.size and float(np.nanmax(array)) <= 1.5 else 1.0
        array = np.clip(array * scale, 0, 255).astype(np.uint8)
    return array


def _depth_float16(value: Any) -> np.ndarray:
    array = _numpy(value)
    if array.ndim == 4:
        array = array[0]
    if array.ndim == 3 and array.shape[-1] == 1:
        array = array[..., 0]
    return array.astype(np.float16)


def _normalize_semantic_label(value: Any) -> str | None:
    text = str(value).strip().lower()
    text = text.replace("'", "").replace('"', "")
    text = text.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
    if "scalpel_type2" in text or "scalpeltype2" in text:
        return "scalpel_type2"
    if "love_retractor" in text or "loveretractor" in text:
        return "love_retractor"
    if "scissor" in text:
        return "scissor"
    if "kelly" in text:
        return "kelly"
    if "scalpel" in text or "knife" in text:
        return "scalpel"
    if any(name in text for name in ("surgical_tray", "surgicaltray", "klt_bin", "kltbin")):
        return "surgical_tray"
    if any(name in text for name in ("robot", "franka", "panda")):
        return "robot"
    if any(name in text for name in ("background", "unlabelled", "unlabeled")):
        return "background"
    return None


def _find_id_to_labels(value: Any) -> dict | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() == "idtolabels" and isinstance(item, dict):
                return item
        for item in value.values():
            result = _find_id_to_labels(item)
            if result is not None:
                return result
    elif isinstance(value, (list, tuple)):
        for item in value:
            result = _find_id_to_labels(item)
            if result is not None:
                return result
    return None


def _metadata_label(value: Any) -> str | None:
    if isinstance(value, dict):
        for key in ("class", "label", "labels", "semanticLabel", "semanticData", "name"):
            if key in value:
                result = _metadata_label(value[key])
                if result is not None:
                    return result
        for item in value.values():
            result = _metadata_label(item)
            if result is not None:
                return result
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            result = _metadata_label(item)
            if result is not None:
                return result
    return _normalize_semantic_label(value)


def _color_tuple(value: Any) -> tuple[int, int, int, int] | None:
    if isinstance(value, (tuple, list)):
        numbers = [int(item) for item in value]
    else:
        numbers = [int(item) for item in re.findall(r"-?\d+", str(value))[:4]]
    if len(numbers) == 3:
        numbers.append(255)
    return tuple(numbers[:4]) if len(numbers) >= 4 else None


def canonical_semantic(cam: Any, height: int, width: int) -> np.ndarray:
    """Convert Isaac semantic output into the teammate's stable class IDs."""

    canonical = np.zeros((height, width), dtype=np.uint16)
    output = cam.data.output
    if "semantic_segmentation" not in output:
        return canonical
    semantic = _numpy(output["semantic_segmentation"])
    if semantic.ndim == 4:
        semantic = semantic[0]
    labels = _find_id_to_labels(getattr(cam.data, "info", None))
    if labels is None:
        return canonical

    if semantic.ndim == 3 and semantic.shape[-1] >= 3:
        rgba = semantic[..., :4]
        if rgba.shape[-1] == 3:
            rgba = np.concatenate(
                (rgba, np.full((*rgba.shape[:2], 1), 255, dtype=rgba.dtype)),
                axis=-1,
            )
        rgba = rgba[:height, :width].astype(np.int32, copy=False)
        for raw_key, metadata in labels.items():
            color = _color_tuple(raw_key)
            name = _metadata_label(metadata)
            if color is not None and name is not None:
                canonical[np.all(rgba == np.asarray(color).reshape(1, 1, 4), axis=-1)] = (
                    SEMANTIC_CLASS_IDS[name]
                )
        return canonical

    if semantic.ndim == 3 and semantic.shape[-1] == 1:
        semantic = semantic[..., 0]
    if semantic.ndim != 2:
        return canonical
    semantic = semantic[:height, :width]
    for raw_key, metadata in labels.items():
        try:
            raw_id = int(raw_key)
        except (TypeError, ValueError):
            continue
        name = _metadata_label(metadata)
        if name is not None:
            canonical[semantic == raw_id] = SEMANTIC_CLASS_IDS[name]
    return canonical


def _base_pose(env: Any, position_w: torch.Tensor, quaternion_w: torch.Tensor) -> torch.Tensor:
    robot = env.scene["robot"]
    position_b = math_utils.quat_apply_inverse(
        robot.data.root_quat_w[0:1],
        position_w.reshape(1, 3) - robot.data.root_pos_w[0:1],
    )[0]
    quaternion_b = math_utils.quat_mul(
        math_utils.quat_inv(robot.data.root_quat_w[0:1]),
        quaternion_w.reshape(1, 4),
    )[0]
    return torch.cat((position_b, quaternion_b), dim=0)


class TeammateHDF5Recorder:
    """Write the original segmented Phase-3 8D, six-camera HDF5 schema."""

    def __init__(
        self,
        output_dir: str | Path,
        task_description: str,
        target: str,
        skill: str,
        spawn: EpisodeSpawn,
        profile: ObjectSkillProfile,
        team_env_dir: str | Path | None = None,
        debug_every: int = 25,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.task_description = task_description
        self.target = target
        self.policy_skill = "pick" if skill in {"pick", "pick_lift"} else "place"
        self.spawn = spawn
        self.profile = profile
        self.debug_every = debug_every

        tuning = _camera_tuning(resolve_team_env_dir(team_env_dir))
        self.camera_width = int(tuning.CAMERA_WIDTH)
        self.camera_height = int(tuning.CAMERA_HEIGHT)
        self.camera_cfg = tuning.PHASE3_CAMERAS
        self.reset_buffers()

    def reset_buffers(self) -> None:
        self.states: list[np.ndarray] = []
        self.robot_proprio: list[np.ndarray] = []
        self.legacy_states: list[np.ndarray] = []
        self.actions: list[np.ndarray] = []
        self.stage_names: list[str] = []
        self.stage_suffixes: list[str] = []
        self.stage_ids: list[int] = []
        self.step_ids: list[int] = []
        self.target_slots_b: list[np.ndarray] = []
        self.rgb = {view: [] for view in CAMERA_VIEWS}
        self.depth = {view: [] for view in CAMERA_VIEWS}
        self.semantic = {view: [] for view in CAMERA_VIEWS}

    def _robot_state(
        self,
        env: Any,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        robot = env.scene["robot"]
        ee_frame = env.scene["ee_frame"]
        ee_frame.update(dt=env.physics_dt)
        ee_pos_w = ee_frame.data.target_pos_w[0, 0].clone()
        ee_quat_w = ee_frame.data.target_quat_w[0, 0].clone()
        ee_pose_b = _base_pose(env, ee_pos_w, ee_quat_w)
        joints = robot.data.joint_pos[0].clone()
        proprio = torch.cat((joints, ee_pose_b), dim=0)

        object_id = float(OBJECT_TYPE_IDS[self.target])
        skill_id = float(SKILL_TYPE_IDS[self.policy_skill])
        state = torch.cat(
            (proprio, torch.tensor((object_id, skill_id), device=env.device)),
            dim=0,
        )

        primary_category = "scissor" if self.target == "scalpel" else self.target
        primary = env.scene[scene_key(primary_category, self.target)]
        scalpel = env.scene[scene_key("scalpel", self.target)]
        primary_pose_b = _base_pose(env, primary.data.root_pos_w[0], primary.data.root_quat_w[0])
        scalpel_pose_b = _base_pose(env, scalpel.data.root_pos_w[0], scalpel.data.root_quat_w[0])
        slot_w = torch.tensor(self.spawn.tray_xyz, device=env.device) + torch.tensor(
            self.profile.tray_slot_offset,
            device=env.device,
        )
        slot_b = math_utils.quat_apply_inverse(
            robot.data.root_quat_w[0:1],
            slot_w.reshape(1, 3) - robot.data.root_pos_w[0:1],
        )[0]
        legacy = torch.cat(
            (
                proprio,
                primary_pose_b,
                scalpel_pose_b,
                slot_b,
                torch.tensor((0.0,), device=env.device),
            ),
            dim=0,
        )
        if proprio.shape[0] != 16 or state.shape[0] != 18 or legacy.shape[0] != 34:
            raise RuntimeError(
                f"Teammate state contract violated: proprio={proprio.shape}, "
                f"state={state.shape}, legacy={legacy.shape}"
            )
        return (
            _numpy(state).astype(np.float32),
            _numpy(proprio).astype(np.float32),
            _numpy(legacy).astype(np.float32),
            _numpy(slot_b).astype(np.float32),
        )

    def add_step(self, step: RecorderStep) -> None:
        state, proprio, legacy, slot_b = self._robot_state(step.env)
        action = _numpy(step.action[0]).astype(np.float32)
        if action.shape != (8,):
            raise RuntimeError(f"Teammate action must be 8D, received {action.shape}")

        camera_payload = {}
        for view in CAMERA_VIEWS:
            cam = step.env.scene[VIEW_TO_SCENE_KEY[view]]
            output = cam.data.output
            if "rgb" not in output or "distance_to_image_plane" not in output:
                raise RuntimeError(f"Camera {view} is missing RGB or depth output")
            camera_payload[view] = (
                _rgb_uint8(output["rgb"]),
                _depth_float16(output["distance_to_image_plane"]),
                canonical_semantic(cam, self.camera_height, self.camera_width),
            )

        prefix = STAGE_PREFIX[self.target]
        self.states.append(state)
        self.robot_proprio.append(proprio)
        self.legacy_states.append(legacy)
        self.target_slots_b.append(slot_b)
        self.actions.append(action)
        self.stage_names.append(f"{prefix}_{step.stage_suffix}")
        self.stage_suffixes.append(step.stage_suffix)
        self.stage_ids.append(STAGE_TYPE_IDS[step.stage_suffix])
        self.step_ids.append(step.step_id)
        for view, (rgb, depth, semantic) in camera_payload.items():
            self.rgb[view].append(rgb)
            self.depth[view].append(depth)
            self.semantic[view].append(semantic)

        count = len(self.actions)
        if count == 1 or (self.debug_every > 0 and count % self.debug_every == 0):
            print(f"[TEAMMATE REC step={count:04d}] stage={self.stage_names[-1]}")

    def save_episode(self, episode_id: int, metadata: dict[str, Any] | None = None) -> str | None:
        if not self.actions:
            print("[TeammateRecorder] Buffer empty, nothing to save.")
            return None

        states = np.asarray(self.states, dtype=np.float32)
        proprio = np.asarray(self.robot_proprio, dtype=np.float32)
        legacy = np.asarray(self.legacy_states, dtype=np.float32)
        actions = np.asarray(self.actions, dtype=np.float32)
        slots = np.asarray(self.target_slots_b, dtype=np.float32)
        count = len(actions)
        dones = np.zeros((count,), dtype=np.bool_)
        dones[-1] = True

        if states.shape != (count, 18) or actions.shape != (count, 8):
            raise RuntimeError(
                f"Teammate HDF5 contract violated: state={states.shape}, actions={actions.shape}"
            )

        filename = self.output_dir / f"episode_{episode_id:06d}.h5"
        with h5py.File(filename, "w") as stream:
            stream.attrs["dataset_schema"] = "phase3_vision_pickplace_no_slot_v2"
            stream.attrs["policy_skill"] = self.policy_skill
            stream.attrs["target_object"] = self.target
            stream.attrs["object_type_id"] = OBJECT_TYPE_IDS[self.target]
            stream.attrs["skill_id"] = SKILL_TYPE_IDS[self.policy_skill]
            stream.attrs["success"] = True
            stream.attrs["num_samples"] = count
            stream.attrs["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stream.attrs["language_instruction"] = self.task_description
            stream.attrs["task_description"] = self.task_description
            stream.attrs["state_dim"] = 18
            stream.attrs["action_dim"] = 8
            stream.attrs["state_keys"] = json.dumps(REALCOMPAT_STATE_KEYS)
            stream.attrs["action_keys"] = json.dumps(ACTION_KEYS)
            stream.attrs["object_type_ids"] = json.dumps(OBJECT_TYPE_IDS)
            stream.attrs["skill_type_ids"] = json.dumps(SKILL_TYPE_IDS)
            stream.attrs["stage_type_ids"] = json.dumps(STAGE_TYPE_IDS)
            stream.attrs["state_frame"] = "robot_base"
            stream.attrs["action_frame"] = "robot_base"
            stream.attrs["action_type"] = "absolute_pose_quat_gripper_8d_baseframe"
            stream.attrs["camera_views"] = json.dumps(list(CAMERA_VIEWS))
            stream.attrs["camera_rgb_shape"] = json.dumps(
                [self.camera_height, self.camera_width, 3]
            )
            stream.attrs["camera_depth_shape"] = json.dumps(
                [self.camera_height, self.camera_width]
            )
            stream.attrs["depth_type"] = "distance_to_image_plane_meters_float16"
            stream.attrs["semantic_mapping_version"] = "phase3_canonical_v1"
            stream.attrs["semantic_class_ids"] = json.dumps(SEMANTIC_CLASS_IDS)
            stream.attrs["important"] = (
                "Policy-safe observations exclude simulator ground-truth object poses. "
                "GT is stored only under debug_gt."
            )
            grip = self.camera_cfg["grip_cam_b"]
            stream.attrs["grip_b_camera_prim"] = grip["prim_path"]
            stream.attrs["grip_b_pos"] = json.dumps(list(grip["pos"]))
            stream.attrs["grip_b_rot"] = json.dumps(list(grip["rot"]))
            stream.attrs["grip_b_rot90_k"] = 0
            for key, value in (metadata or {}).items():
                try:
                    stream.attrs[key] = (
                        value
                        if isinstance(value, (str, int, float, bool))
                        else json.dumps(value)
                    )
                except TypeError:
                    stream.attrs[key] = str(value)

            observations = stream.create_group("observations")
            observations.create_dataset("state", data=states)
            observations.create_dataset("robot_proprio", data=proprio)
            observations.create_dataset(
                "object_type_id",
                data=np.full((count, 1), OBJECT_TYPE_IDS[self.target], dtype=np.float32),
            )
            observations.create_dataset(
                "skill_id",
                data=np.full((count, 1), SKILL_TYPE_IDS[self.policy_skill], dtype=np.float32),
            )
            observations.create_dataset(
                "stage_id",
                data=np.asarray(self.stage_ids, dtype=np.int32).reshape(-1, 1),
            )

            front_rgb = np.asarray(self.rgb["front"], dtype=np.uint8)
            front_depth = np.asarray(self.depth["front"], dtype=np.float16)
            front_semantic = np.asarray(self.semantic["front"], dtype=np.uint16)
            wrist_rgb = np.asarray(self.rgb["grip_b"], dtype=np.uint8)
            wrist_depth = np.asarray(self.depth["grip_b"], dtype=np.float16)
            wrist_semantic = np.asarray(self.semantic["grip_b"], dtype=np.uint16)

            observations.create_dataset("front_rgb", data=front_rgb, compression="gzip")
            observations.create_dataset("front_depth", data=front_depth, compression="gzip")
            observations.create_dataset("front_semantic", data=front_semantic, compression="gzip")
            observations.create_dataset("wrist_rgb", data=wrist_rgb, compression="gzip")
            observations.create_dataset("wrist_depth", data=wrist_depth, compression="gzip")
            observations.create_dataset("images_front", data=front_rgb, compression="gzip")
            observations.create_dataset("depth_front", data=front_depth, compression="gzip")
            observations.create_dataset("images_wrist", data=wrist_rgb, compression="gzip")
            observations.create_dataset("depth_wrist", data=wrist_depth, compression="gzip")
            observations.create_dataset("images_grip_b", data=wrist_rgb, compression="gzip")
            observations.create_dataset("depth_grip_b", data=wrist_depth, compression="gzip")
            observations.create_dataset("grip_b_semantic", data=wrist_semantic, compression="gzip")
            observations.create_dataset("segmentation_map", data=front_semantic, compression="gzip")

            for view in ("cam_top", "cam_left", "cam_right", "cam_tray"):
                observations.create_dataset(
                    f"{view}_rgb",
                    data=np.asarray(self.rgb[view], dtype=np.uint8),
                    compression="gzip",
                )
                observations.create_dataset(
                    f"{view}_depth",
                    data=np.asarray(self.depth[view], dtype=np.float16),
                    compression="gzip",
                )
                observations.create_dataset(
                    f"{view}_semantic",
                    data=np.asarray(self.semantic[view], dtype=np.uint16),
                    compression="gzip",
                )

            stream.create_dataset("actions", data=actions)
            stream.create_dataset("dones", data=dones)
            stream.create_dataset("rewards", data=np.zeros((count,), dtype=np.float32))
            stream.create_dataset(
                "stage_names",
                data=np.asarray(self.stage_names, dtype=h5py.string_dtype()),
            )
            stream.create_dataset(
                "stage_suffixes",
                data=np.asarray(self.stage_suffixes, dtype=h5py.string_dtype()),
            )
            stream.create_dataset("step_ids", data=np.asarray(self.step_ids, dtype=np.int32))

            debug = stream.create_group("debug_gt")
            debug.create_dataset("target_slot_b", data=slots)
            debug.create_dataset("legacy_state_34d", data=legacy)
            primary_category = "scissor" if self.target == "scalpel" else self.target
            debug.create_dataset(f"{primary_category}_pose_b", data=legacy[:, 16:23])
            debug.create_dataset("scalpel_pose_b", data=legacy[:, 23:30])
            selected = legacy[:, 23:30] if self.target == "scalpel" else legacy[:, 16:23]
            debug.create_dataset("selected_object_pose_b", data=selected)

            stats = stream.create_group("norm_stats")
            stats.create_dataset("state_mean", data=states.mean(0).astype(np.float32))
            stats.create_dataset("state_std", data=(states.std(0) + 1.0e-8).astype(np.float32))
            stats.create_dataset("action_mean", data=actions.mean(0).astype(np.float32))
            stats.create_dataset("action_std", data=(actions.std(0) + 1.0e-8).astype(np.float32))

        validate_teammate_episode(filename)
        print(f"[TeammateRecorder] Saved and validated {count} steps to: {filename}")
        self.reset_buffers()
        return str(filename)


def write_dataset_norm_stats(output_dir: str | Path) -> Path | None:
    """Write the same dataset-level JSON statistics as the original recorders."""

    root = Path(output_dir)
    files = sorted(root.glob("episode_*.h5"))
    if not files:
        return None
    states = []
    actions = []
    for filename in files:
        with h5py.File(filename, "r") as stream:
            states.append(stream["observations/state"][:])
            actions.append(stream["actions"][:])
    state = np.concatenate(states, axis=0)
    action = np.concatenate(actions, axis=0)
    payload = {
        "state": {
            "mean": state.mean(0).tolist(),
            "std": (state.std(0) + 1.0e-8).tolist(),
            "min": state.min(0).tolist(),
            "max": state.max(0).tolist(),
        },
        "action": {
            "mean": action.mean(0).tolist(),
            "std": (action.std(0) + 1.0e-8).tolist(),
            "min": action.min(0).tolist(),
            "max": action.max(0).tolist(),
        },
        "state_keys": REALCOMPAT_STATE_KEYS,
        "action_keys": ACTION_KEYS,
        "state_dim": 18,
        "action_dim": 8,
        "num_episodes": len(files),
        "total_steps": int(state.shape[0]),
        "dataset_schema": "phase3_realcompatible_split_skill_v1",
    }
    destination = root / "norm_stats.json"
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination
