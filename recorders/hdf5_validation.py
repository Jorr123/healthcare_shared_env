"""Fast, simulator-independent checks for the two shared HDF5 contracts."""

from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np


TEAMMATE_CAMERA_DATASETS = {
    "front": ("front_rgb", "front_depth", "front_semantic"),
    "grip_b": ("wrist_rgb", "wrist_depth", "grip_b_semantic"),
    "cam_top": ("cam_top_rgb", "cam_top_depth", "cam_top_semantic"),
    "cam_left": ("cam_left_rgb", "cam_left_depth", "cam_left_semantic"),
    "cam_right": ("cam_right_rgb", "cam_right_depth", "cam_right_semantic"),
    "cam_tray": ("cam_tray_rgb", "cam_tray_depth", "cam_tray_semantic"),
}


def _require_shape(dataset: h5py.Dataset, shape: tuple[int, ...], label: str) -> None:
    if dataset.shape != shape:
        raise RuntimeError(f"{label} has shape {dataset.shape}; expected {shape}")


def _require_binary_gripper(actions: h5py.Dataset, column: int, label: str) -> None:
    values = np.asarray(actions[:, column])
    if not np.isin(values, (-1.0, 1.0)).all():
        raise RuntimeError(f"{label} contains non-binary gripper values")


def validate_openvla_episode(path: str | Path) -> None:
    """Validate the shared 7D OpenVLA episode without loading its images."""

    filename = Path(path)
    with h5py.File(filename, "r") as stream:
        required = (
            "observations/images",
            "observations/wrist_images",
            "observations/proprio",
            "actions",
        )
        missing = [key for key in required if key not in stream]
        if missing:
            raise RuntimeError(f"{filename} is missing OpenVLA datasets: {missing}")

        count = stream["actions"].shape[0]
        _require_shape(stream["actions"], (count, 7), "OpenVLA actions")
        _require_shape(
            stream["observations/images"],
            (count, 224, 224, 3),
            "OpenVLA primary images",
        )
        _require_shape(
            stream["observations/wrist_images"],
            (count, 336, 448, 3),
            "OpenVLA wrist images",
        )
        _require_shape(stream["observations/proprio"], (count, 7), "OpenVLA proprio")
        if stream["observations/images"].dtype != np.uint8:
            raise RuntimeError("OpenVLA primary images must be uint8")
        _require_binary_gripper(stream["actions"], 6, "OpenVLA actions")


def validate_teammate_episode(path: str | Path) -> None:
    """Validate the original teammate 8D/six-camera episode contract."""

    filename = Path(path)
    with h5py.File(filename, "r") as stream:
        if stream.attrs.get("dataset_schema") != "phase3_vision_pickplace_no_slot_v2":
            raise RuntimeError(f"{filename} has the wrong teammate dataset schema")
        if stream.attrs.get("action_type") != "absolute_pose_quat_gripper_8d_baseframe":
            raise RuntimeError(f"{filename} has the wrong teammate action type")

        required = (
            "observations/state",
            "observations/robot_proprio",
            "observations/stage_id",
            "actions",
            "dones",
            "rewards",
            "stage_names",
            "stage_suffixes",
            "step_ids",
            "debug_gt/target_slot_b",
            "debug_gt/legacy_state_34d",
            "norm_stats/state_mean",
            "norm_stats/action_mean",
        )
        missing = [key for key in required if key not in stream]
        if missing:
            raise RuntimeError(f"{filename} is missing teammate datasets: {missing}")

        count = stream["actions"].shape[0]
        _require_shape(stream["actions"], (count, 8), "Teammate actions")
        _require_shape(stream["observations/state"], (count, 18), "Teammate state")
        _require_shape(
            stream["observations/robot_proprio"],
            (count, 16),
            "Teammate robot proprio",
        )
        _require_shape(stream["observations/stage_id"], (count, 1), "Teammate stage IDs")
        _require_shape(stream["dones"], (count,), "Teammate dones")
        _require_shape(stream["rewards"], (count,), "Teammate rewards")
        _require_shape(stream["stage_names"], (count,), "Teammate stage names")
        _require_shape(stream["stage_suffixes"], (count,), "Teammate stage suffixes")
        _require_shape(stream["step_ids"], (count,), "Teammate step IDs")

        observations = stream["observations"]
        for view, (rgb_key, depth_key, semantic_key) in TEAMMATE_CAMERA_DATASETS.items():
            for key in (rgb_key, depth_key, semantic_key):
                if key not in observations:
                    raise RuntimeError(f"{filename} is missing {view} dataset: {key}")
            _require_shape(
                observations[rgb_key],
                (count, 336, 448, 3),
                f"Teammate {view} RGB",
            )
            _require_shape(
                observations[depth_key],
                (count, 336, 448),
                f"Teammate {view} depth",
            )
            _require_shape(
                observations[semantic_key],
                (count, 336, 448),
                f"Teammate {view} semantic",
            )
            if observations[rgb_key].dtype != np.uint8:
                raise RuntimeError(f"Teammate {view} RGB must be uint8")
            if observations[depth_key].dtype != np.float16:
                raise RuntimeError(f"Teammate {view} depth must be float16")
            if observations[semantic_key].dtype != np.uint16:
                raise RuntimeError(f"Teammate {view} semantic must be uint16")

        quaternions = np.asarray(stream["actions"][:, 3:7])
        norms = np.linalg.norm(quaternions, axis=1)
        if not np.allclose(norms, 1.0, atol=1.0e-3):
            raise RuntimeError(f"{filename} contains non-unit action quaternions")
        _require_binary_gripper(stream["actions"], 7, "Teammate actions")
