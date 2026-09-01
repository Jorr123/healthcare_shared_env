
# ---- SCALPEL_TYPE2 unified target+distractor config ----
from phase3_shared_env_cfg import RecorderEnvRequest, apply_shared_env_cfg, apply_workspace_globals, asset_path

ENV_REQUEST = RecorderEnvRequest(
    target="scalpel_type2",
    distractors=("scalpel", "scissor", "love_retractor", "kelly"),
    environment=None,
    use_canonical_target_only=True,
)

SCALPEL_TYPE2_USD_PATH = asset_path("scalpel_type2_root.usd")

# Same size for target object and distractor. Increase this if the bigger visual is the desired one.
SCALPEL_TYPE2_SCALE = (0.00715074, 0.00715074, 0.00715074)
SCALPEL_TYPE2_SPAWN_ROOT_Z = 0.0120

# Legacy aliases for copied code.


def phase3_scene_key_for_object(obj_name):
    return "scalpel_type2" if obj_name == "scalpel_type2" else obj_name

SCISSOR_SPAWN_ROOT_Z = 0.0025
SCALPEL_USD = asset_path("knife_centered.usd")
TRAY_USD = asset_path("SurgicalTray.usd")

SCISSOR_USD = asset_path("my_scissor_clean.usd")
SCISSOR_SCALE = (0.01, 0.01, 0.01)
LOVE_USD_PATH = asset_path("love_centered_root_at_center.usd")
LOVE_SCALE = (0.00075, 0.00075, 0.00075)
LOVE_SPAWN_ROOT_Z = 0.0010
SETTLE_STEPS      = 150
SETTLE_VEL_THRESH = 0.003
SETTLE_POLL_EVERY = 10
SETTLE_CONSEC_OK  = 3

TABLE_Z = 0.0

# ScalpelType2: keep old working grasp logic.
SCALPEL_TYPE2_GRASP_ABOVE_TABLE = 0.005
SCALPEL_TYPE2_GRASP_YAW_OFFSET_DEG = 90.0
SCALPEL_TYPE2_BODY_OFFSET_X = 0.0
SCALPEL_TYPE2_BODY_OFFSET_Y = 0.0
SCALPEL_TYPE2_BODY_OFFSET_Z = 0.000

# Compatibility aliases: internal scene key stays "scalpel_type2"; dataset-visible object is "scalpel_type2".


# Scalpel: verified values from the random-spawn debug script.
SCALPEL_GRASP_Z_ABOVE_TABLE = 0.007
SCALPEL_GRASP_Z_MIN = 0.004
SCALPEL_GRASP_Z_MAX = 0.015
SCALPEL_LOWER_EXTRA_Z = 0.004

# This is the verified local body-center offset for knife_centered.usd.
# Target is NOT a fixed world point: world center = root + quat_apply(root_quat, SCALPEL_LOCAL_CENTER).
SCALPEL_LOCAL_CENTER = (0.0, 0.0656, 0.0)

# Keep these aliases only for old metadata compatibility.
SCALPEL_BODY_OFFSET_X = SCALPEL_LOCAL_CENTER[0]
SCALPEL_BODY_OFFSET_Y = SCALPEL_LOCAL_CENTER[1]
SCALPEL_BODY_OFFSET_Z = SCALPEL_LOCAL_CENTER[2]

# Scalpel pose modes:
# - BROAD_FLAT: broad face flat on table; local +Y points down/up, local X/Z lie in table plane.
# - EDGE_SIDE: scalpel stands on its side/edge; local X points up, local Y lies in table plane.
# For dataset stability, leave both. To collect flat-only, set ["BROAD_FLAT"].
SCALPEL_POSE_SEQUENCE = ["BROAD_FLAT", "EDGE_SIDE"]
SCALPEL_FLAT_LONG_AXIS = "X"   # verified good for BROAD_FLAT
SCALPEL_EDGE_LONG_AXIS = "Y"   # verified good for EDGE_SIDE
SCALPEL_GRASP_YAW_OFFSET = 0.0

SCALPEL_FLAT_Y_AXIS_MIN_Z = 0.65
SCALPEL_EDGE_X_AXIS_MIN_Z = 0.65
SCALPEL_BROAD_CENTER_Z = 0.0008
SCALPEL_EDGE_CENTER_Z  = 0.0038

# Direct randomized spawn.
FORCE_OBJECTS_DIRECT_AFTER_RESET = True
RANDOM_SEED = None

SCALPEL_TYPE2_RANDOM_X_RANGE = (0.34, 0.64)
SCALPEL_TYPE2_RANDOM_Y_RANGE = (0.04, 0.32)
LOVE_RANDOM_X_RANGE = (0.34, 0.64)
LOVE_RANDOM_Y_RANGE = (0.04, 0.32)
SCALPEL_RANDOM_CENTER_X_RANGE = (0.48, 0.64)
SCALPEL_RANDOM_CENTER_Y_RANGE = (0.08, 0.32)
RANDOM_YAW_DEG_RANGE = (0.0, 360.0)

# =============================================================================
# Phase 3 grid recording setup
# =============================================================================
# 2D grid used for dataset coverage. Target object is placed cell-by-cell.

# SCALPEL_TYPE2 RETRACTOR ASSET OVERRIDE
KELLY_USD_PATH = asset_path("kelly_root_at_center.usd")
KELLY_SCALE = (0.60, 0.60, 0.60)
KELLY_SPAWN_ROOT_Z = 0.0140
SCALPEL_TYPE2_YAW_DEG = 0.0
SCALPEL_TYPE2_PLACE_Z = 0.020
SCALPEL_TYPE2_LIFT_Z = 0.140
SCALPEL_TYPE2_CONTACT_Z = 0.010
SCALPEL_TYPE2_GRASP_Z_FRAC = 0.50
OBJECT_TYPE_ID = 4

GRID_COLS = 5
GRID_ROWS = 4
GRID_X_RANGE = (0.34, 0.64)
GRID_Y_RANGE = (0.04, 0.32)

# Visual-only grid. Does not affect object spawn.
# This is only to make the grid look large on the table.
VIS_GRID_COLS = 5
VIS_GRID_ROWS = 4
VIS_GRID_X_RANGE = (0.28, 0.98)
VIS_GRID_Y_RANGE = (-0.02, 0.44)


# Visual grid shown during recording using debug_draw.
SHOW_GRID_DEBUG_MARKERS = False

# Current assets only support one distractor object:
# if target=scalpel -> distractor=scalpel_type2
# if target=scalpel_type2 -> distractor=scalpel
REQUESTED_NUM_DISTRACTORS = 3

ALL_PHASE3_OBJECTS = ("scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2")
# Object IDs for policy conditioning.
OBJECT_TYPE_IDS = {
    "scalpel": 0,
    "scissor": 1,
    "love_retractor": 2,
    "kelly": 3,
    "scalpel_type2": 4,
}
SKILL_TYPE_IDS = {
    "pick": 0,
    "place": 1,
}
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
    "joint_pos_0","joint_pos_1","joint_pos_2","joint_pos_3",
    "joint_pos_4","joint_pos_5","joint_pos_6",
    "finger_pos_0","finger_pos_1",
    "ee_pos_bx","ee_pos_by","ee_pos_bz",
    "ee_quat_bw","ee_quat_bx","ee_quat_by","ee_quat_bz",
    "object_type_id",
    "skill_id",
]
REALCOMPAT_STATE_DIM = len(REALCOMPAT_STATE_KEYS)

PICK_STAGE_SUFFIXES = {
    "OPEN_HOVER", "LOWER_PRE", "LOWER_GRASP", "LOWER_EXTRA",
    "HOLD_BEFORE_CLOSE", "CLOSE", "HOLD_AFTER_CLOSE",
    "MICRO_LIFT", "LIFT_MID", "LIFT",
}
PLACE_STAGE_SUFFIXES = {
    "MOVE_PLACE", "LOWER_PLACE", "OPEN", "RETREAT",
}


SPAWN_MAX_TRIES = 400
# Relaxed a bit: object-object can be closer, but still avoid direct overlap.
SPAWN_MIN_OBJ_OBJ  = 0.105
SPAWN_MIN_OBJ_TRAY = 0.15

# Phase 3: fixed tray, placed farther from the pick grid.
USE_FIXED_TRAY = True
TRAY_FIXED_POS = (0.34, -0.26, 0.006)
TRAY_FIXED_YAW_DEG = 90.0

# Kept only for old compatibility. Not used when USE_FIXED_TRAY=True.
TRAY_RANDOM_X_RANGE = (0.36, 0.66)
TRAY_RANDOM_Y_RANGE = (-0.20, 0.20)

SCALPEL_TYPE2_SLOT_OFFSET = [0.0,  0.055, 0.025]
SCALPEL_SLOT_OFFSET = [0.0, -0.055, 0.025]

# Common lower bound for any grasp target. Do not use negative Z for the scalpel.
GRASP_Z_MIN = 0.003

MIN_INTERP_STEPS   = 12
SLERP_FALLBACK_DOT = 0.9995

# Turn ON only for debug checking. Keep OFF for clean dataset images.
SHOW_MARKERS = False
MARKER_COLORS = {
    "hover":(0.2,0.8,1.0,0.85),"pre":(0.4,1.0,0.4,0.85),
    "grasp":(1.0,0.9,0.0,1.00),"micro_lift":(1.0,0.5,0.0,0.85),
    "lift_mid":(1.0,0.3,0.3,0.75),"lift":(1.0,0.1,0.1,0.75),
    "place_above":(0.6,0.2,1.0,0.75),"lower":(0.9,0.1,0.9,0.85),
    "retreat":(0.5,0.5,0.5,0.60),"slot":(0.1,1.0,0.5,1.00),
    "obj_origin":(1.0,1.0,1.0,1.00),"obj_grasp_xy":(1.0,0.9,0.0,1.00),
    "body_center":(1.0,0.0,1.0,1.00),"x_axis":(1.0,0.0,0.0,1.00),
    "z_axis":(0.0,0.2,1.0,1.00),
}
MARKER_RADIUS = {
    "grasp":0.018,"obj_origin":0.012,"obj_grasp_xy":0.015,"slot":0.020,
    "body_center":0.012,"x_axis":0.010,"z_axis":0.010,"default":0.010
}

STATE_DIM  = 34
ACTION_DIM = 8

# Camera recording setup
# observations/images remains the front RGB camera for backward compatibility.
# Final setup: front RGB-D + selected grip_b RGB-D only.
# FINAL Phase3 recorder resolution: single source of truth = camera tuner
try:
    from phase3_camera_tuning import CAMERA_WIDTH
    from phase3_camera_tuning import CAMERA_HEIGHT
except ImportError:
    import importlib.util as _p3_importlib_util
    from pathlib import Path as _P3Path

    _p3_tuner_path = _P3Path(__file__).with_name("phase3_camera_tuning.py")
    _p3_spec = _p3_importlib_util.spec_from_file_location(
        "phase3_camera_tuning_runtime",
        _p3_tuner_path,
    )
    _p3_mod = _p3_importlib_util.module_from_spec(_p3_spec)
    _p3_spec.loader.exec_module(_p3_mod)

    CAMERA_WIDTH = int(_p3_mod.CAMERA_WIDTH)
    CAMERA_HEIGHT = int(_p3_mod.CAMERA_HEIGHT)

print(f"[CAMERA RESOLUTION SOURCE] tuner -> {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
CAMERA_DATA_TYPES = ["rgb", "distance_to_image_plane"]
GRIP_CAM_PARENT = "{ENV_REGEX_NS}/Robot/panda_hand"

# Final selected gripper camera: grip_b from the center-gap test.
GRIP_B_CAMERA_PRIM = f"{GRIP_CAM_PARENT}/GripCamB_Final"

# Rotate saved grip_b RGB/depth image to make it upright.
# If preview becomes rotated the wrong way, change 1 -> 3.
GRIP_B_ROT90_K = 0

# Preview PNG export:
# False = export stage transitions + every CAMERA_EXPORT_STRIDE steps.
# True  = export every frame as PNG. Much heavier.
EXPORT_ALL_PNG_STEPS = False
CAMERA_EXPORT_STRIDE = 50

import argparse, os, json, glob, math
import h5py
import numpy as np
import torch
from datetime import datetime
from collections import Counter
from PIL import Image

# ---- scalpel_type2 target asset; internal legacy scene key remains "scalpel_type2" ----

# Compatibility aliases for old internal code.


# === PHASE3 FINAL MULTI-CAMERA RECORDER PATCH ===
from phase3_recorder_camera_patch import (
    PHASE3_EXTRA_CAMERA_NAMES,
    PHASE3_ALL_CAMERA_VIEWS,
    phase3_apply_final_cameras_to_env_cfg,
    phase3_safe_semantic,
    phase3_dump_runtime_alignment,
)
# === END PHASE3 FINAL MULTI-CAMERA RECORDER PATCH ===

from isaaclab.app import AppLauncher

# ============================================================
# PHASE3 RECORD MODE - EARLY, before argparse print hooks
# ============================================================
def phase3_get_record_mode():
    import sys
    argv = list(sys.argv)

    for i, a in enumerate(argv):
        if a == "--record_mode" and i + 1 < len(argv):
            return str(argv[i + 1]).lower().strip()
        if str(a).startswith("--record_mode="):
            return str(a).split("=", 1)[1].lower().strip()

    return str(globals().get("PHASE3_RECORD_MODE", "both")).lower().strip()


parser = argparse.ArgumentParser()

parser.add_argument("--record_mode", type=str, default="both", choices=["both", "pick", "place"], help="Which H5 segments to save: both, pick, or place. Full episode still runs.")
parser.add_argument("--task",          type=str, default="Isaac-Lift-Cube-Franka-IK-Abs-v0")
parser.add_argument("--num_envs",      type=int, default=1)
parser.add_argument("--episodes",      type=int, default=1)
parser.add_argument("--out_dir",       type=str, default="datasets/phase3_grid_split")
parser.add_argument("--task_text",     type=str,
    default="Pick up the surgical scalpel_type2 and place it in the left tray slot")
parser.add_argument("--debug_every",   type=int, default=25)
parser.add_argument("--resume",        action="store_true")
parser.add_argument("--save_every",    type=int, default=50)
parser.add_argument("--wandb",         action="store_true")
parser.add_argument("--wandb_project", type=str, default="dual-tray-recording")
parser.add_argument("--wandb_run",     type=str, default="dual_demos")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
globals()["PHASE3_RECORD_MODE"] = str(getattr(args_cli, "record_mode", "both")).lower().strip()
globals()["PHASE3_OUT_DIR"] = str(getattr(args_cli, "out_dir", "datasets/phase3_out"))
print(f"[PHASE3_OUT_DIR SET] {globals().get('PHASE3_OUT_DIR')}")
print(f"[PHASE3 RECORD_MODE SET] {globals().get('PHASE3_RECORD_MODE', 'both')}")
print(f"[PHASE3 RECORD_MODE ARGV] {phase3_get_record_mode()}")
args_cli.enable_cameras = True

app_launcher   = AppLauncher(args_cli)
simulation_app = app_launcher.app

import gymnasium as gym
import omni.usd
from pxr import UsdGeom, Gf
try:
    from pxr import Semantics
except Exception:
    Semantics = None

from isaaclab.sensors import CameraCfg
import isaaclab.sim as sim_utils
import isaaclab_tasks
from isaaclab_tasks.utils import parse_env_cfg
from isaaclab.utils.math import quat_apply, quat_inv, quat_mul

STATE_KEYS = [
    "joint_pos_0","joint_pos_1","joint_pos_2","joint_pos_3",
    "joint_pos_4","joint_pos_5","joint_pos_6",
    "finger_pos_0","finger_pos_1",
    "ee_pos_bx","ee_pos_by","ee_pos_bz",
    "ee_quat_bw","ee_quat_bx","ee_quat_by","ee_quat_bz",
    "scalpel_type2_pos_bx","scalpel_type2_pos_by","scalpel_type2_pos_bz",
    "scalpel_type2_quat_bw","scalpel_type2_quat_bx","scalpel_type2_quat_by","scalpel_type2_quat_bz",
    "scalpel_pos_bx","scalpel_pos_by","scalpel_pos_bz",
    "scalpel_quat_bw","scalpel_quat_bx","scalpel_quat_by","scalpel_quat_bz",
    "active_target_bx","active_target_by","active_target_bz",
    "phase_id",
]
ACTION_KEYS = ["x_b","y_b","z_b","qw_b","qx_b","qy_b","qz_b","gripper"]
assert len(STATE_KEYS) == STATE_DIM
assert len(ACTION_KEYS) == ACTION_DIM


# =============================================================================
# Markers (identical to ok_dual_1)
# =============================================================================

_marker_registry: dict = {}

# =============================================================================
# Dataset visual-debug visibility control
# =============================================================================
RECORD_DEBUG_VISUALS = False
SHOW_GRID_DEBUG_MARKERS = False
SHOW_MARKERS = False
SHOW_TARGET_MARKERS = False
SHOW_WAYPOINT_MARKERS = False

# =============================================================================
# PHASE3 CANONICAL SEMANTIC
# Stable IDs for training. Never train on Isaac's raw RGBA / random palette IDs.
# =============================================================================

PHASE3_SEMANTIC_CLASS_IDS = {
    "background": 0,
    "robot": 1,
    "surgical_tray": 2,
    "scalpel": 3,
    "scissor": 4,
    "love_retractor": 5,
    "kelly": 6,
    "scalpel_type2": 7,
}

PHASE3_SEMANTIC_ID_TO_CLASS = {
    0: "background",
    1: "robot",
    2: "surgical_tray",
    3: "scalpel",
    4: "scissor",
    5: "love_retractor",
    6: "kelly",
    7: "scalpel_type2",
}

_SEM_WARNED_KEYS = set()


def _phase3_normalize_semantic_label(label):
    s = str(label).strip().lower()

    # common wrappers produced by semantic metadata
    s = s.replace("'", "").replace('"', "")
    s = s.replace("[", "").replace("]", "")
    s = s.replace("{", "").replace("}", "")

    if "scalpel_type2" in s or "scalpeltype2" in s:
        return "scalpel_type2"

    if "love_retractor" in s or "loveretractor" in s:
        return "love_retractor"

    if "scissor" in s:
        return "scissor"

    if "kelly" in s:
        return "kelly"

    if "scalpel" in s or "knife" in s:
        return "scalpel"

    # SurgicalTray asset carried old semantic klt_bin.
    if (
        "surgical_tray" in s
        or "surgicaltray" in s
        or "klt_bin" in s
        or "kltbin" in s
    ):
        return "surgical_tray"

    # Includes Franka links / hand / fingers when metadata resolves to robot.
    if "robot" in s or "franka" in s or "panda" in s:
        return "robot"

    if "background" in s or "unlabelled" in s or "unlabeled" in s:
        return "background"

    return None


def _phase3_find_id_to_labels(obj):
    """
    Recursively search Camera.data.info for an idToLabels dictionary.
    IsaacLab versions differ: info may be dict, list, tuple, nested dict, etc.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() == "idtolabels" and isinstance(v, dict):
                return v

        for v in obj.values():
            out = _phase3_find_id_to_labels(v)
            if out is not None:
                return out

    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out = _phase3_find_id_to_labels(v)
            if out is not None:
                return out

    return None


def _phase3_extract_color_tuple(key):
    """
    Convert idToLabels key into an RGBA tuple where possible.
    Supports tuple/list and strings such as '(152, 14, 98, 255)'.
    """
    import re as _re

    if isinstance(key, (tuple, list)):
        vals = [int(x) for x in key]
        if len(vals) >= 3:
            if len(vals) == 3:
                vals.append(255)
            return tuple(vals[:4])

    nums = _re.findall(r"-?\d+", str(key))

    if len(nums) >= 3:
        vals = [int(x) for x in nums[:4]]
        if len(vals) == 3:
            vals.append(255)
        return tuple(vals)

    return None


def _phase3_label_from_metadata_value(value):
    """
    Extract canonical class from arbitrary idToLabels value.
    Handles strings, lists, dicts, nested dictionaries.
    """
    if isinstance(value, str):
        return _phase3_normalize_semantic_label(value)

    if isinstance(value, dict):
        # Try likely fields first.
        preferred = [
            "class",
            "label",
            "labels",
            "semanticLabel",
            "semanticData",
            "name",
        ]

        for k in preferred:
            if k in value:
                c = _phase3_label_from_metadata_value(value[k])
                if c is not None:
                    return c

        for v in value.values():
            c = _phase3_label_from_metadata_value(v)
            if c is not None:
                return c

    if isinstance(value, (list, tuple, set)):
        for v in value:
            c = _phase3_label_from_metadata_value(v)
            if c is not None:
                return c

    # Last fallback: inspect printable representation.
    return _phase3_normalize_semantic_label(value)


def _phase3_extract_semantic_u16(
    cam_obj,
    height=CAMERA_HEIGHT,
    width=CAMERA_WIDTH,
    cam_name="camera",
):
    """
    Return TRAINING-SAFE canonical semantic mask.

    Output:
        uint16 [H,W]
        0 background
        1 robot
        2 surgical_tray
        3 scalpel
        4 scissor
        5 love_retractor
        6 kelly
        7 scalpel_type2

    Never treats Isaac RGBA palette values as class IDs.
    """
    import numpy as np

    try:
        out = cam_obj.data.output
    except Exception as e:
        key = (cam_name, "no_output")
        if key not in _SEM_WARNED_KEYS:
            _SEM_WARNED_KEYS.add(key)
            print(
                f"[SEM CANON WARN] {cam_name}: cannot access camera output:",
                repr(e),
            )
        return np.zeros((height, width), dtype=np.uint16)

    if "semantic_segmentation" not in out:
        key = (cam_name, "missing_semantic")
        if key not in _SEM_WARNED_KEYS:
            _SEM_WARNED_KEYS.add(key)
            print(
                f"[SEM CANON WARN] {cam_name}: semantic_segmentation missing"
            )
        return np.zeros((height, width), dtype=np.uint16)

    sem = out["semantic_segmentation"]

    try:
        import torch
        if torch.is_tensor(sem):
            sem = sem.detach().cpu().numpy()
    except Exception:
        pass

    sem = np.asarray(sem)

    # Remove env/batch dimension.
    if sem.ndim == 4:
        sem = sem[0]

    canonical = np.zeros((height, width), dtype=np.uint16)

    try:
        info_all = getattr(cam_obj.data, "info", None)
        id_to_labels = _phase3_find_id_to_labels(info_all)

        if id_to_labels is None:
            key = (cam_name, "no_id_to_labels")
            if key not in _SEM_WARNED_KEYS:
                _SEM_WARNED_KEYS.add(key)
                print(
                    f"[SEM CANON WARN] {cam_name}: "
                    "idToLabels not found in camera.data.info"
                )
            return canonical

        # -----------------------------------------------------------------
        # RGBA semantic image: expected format in current Phase3 setup.
        # -----------------------------------------------------------------
        if sem.ndim == 3 and sem.shape[-1] >= 3:
            rgba = sem[..., :4]

            if rgba.shape[-1] == 3:
                alpha = np.full(
                    (*rgba.shape[:2], 1),
                    255,
                    dtype=rgba.dtype,
                )
                rgba = np.concatenate([rgba, alpha], axis=-1)

            rgba = rgba[:height, :width].astype(np.int32, copy=False)

            discovered = {}

            for raw_key, metadata_value in id_to_labels.items():
                color = _phase3_extract_color_tuple(raw_key)
                class_name = _phase3_label_from_metadata_value(
                    metadata_value
                )

                if color is None or class_name is None:
                    continue

                class_id = PHASE3_SEMANTIC_CLASS_IDS[class_name]

                color_arr = np.asarray(
                    color,
                    dtype=np.int32,
                ).reshape(1, 1, 4)

                match = np.all(rgba == color_arr, axis=-1)

                canonical[match] = class_id

                discovered[color] = (
                    class_name,
                    class_id,
                    int(match.sum()),
                )

            key = (cam_name, "canon_ok")
            if key not in _SEM_WARNED_KEYS:
                _SEM_WARNED_KEYS.add(key)
                print(
                    f"[SEM CANON OK] {cam_name}: "
                    f"shape={canonical.shape} "
                    f"ids={np.unique(canonical).tolist()}"
                )

                for color, data in sorted(discovered.items()):
                    cls, cid, pixels = data
                    print(
                        f"    rgba={color} -> "
                        f"{cls} ({cid}) pixels={pixels}"
                    )

            return canonical

        # -----------------------------------------------------------------
        # Single-channel fallback.
        # Only accepted when idToLabels itself is integer-keyed.
        # -----------------------------------------------------------------
        if sem.ndim == 3 and sem.shape[-1] == 1:
            sem = sem[..., 0]
        elif sem.ndim == 3:
            sem = sem[0]

        if sem.ndim != 2:
            raise RuntimeError(
                f"Unsupported semantic shape {sem.shape}"
            )

        sem = sem[:height, :width]

        for raw_key, metadata_value in id_to_labels.items():
            try:
                raw_id = int(raw_key)
            except Exception:
                continue

            class_name = _phase3_label_from_metadata_value(
                metadata_value
            )

            if class_name is None:
                continue

            canonical[sem == raw_id] = (
                PHASE3_SEMANTIC_CLASS_IDS[class_name]
            )

        key = (cam_name, "canon_single_ok")
        if key not in _SEM_WARNED_KEYS:
            _SEM_WARNED_KEYS.add(key)
            print(
                f"[SEM CANON OK] {cam_name}: "
                f"single-channel ids="
                f"{np.unique(canonical).tolist()}"
            )

        return canonical

    except Exception as e:
        key = (cam_name, "canonicalize_fail")
        if key not in _SEM_WARNED_KEYS:
            _SEM_WARNED_KEYS.add(key)
            print(
                f"[SEM CANON ERROR] {cam_name}:",
                repr(e),
            )

        return canonical


def phase3_expected_distractors():
    return [x for x in PHASE3_ALL_OBJECTS if x != PHASE3_TARGET_OBJECT]

def phase3_validate_spawn_set(spawn_params):
    expected = set(PHASE3_ALL_OBJECTS)
    got = set([PHASE3_TARGET_OBJECT])

    for k in PHASE3_ALL_OBJECTS:
        if k in spawn_params:
            got.add(k)

    missing = sorted(expected - got)
    extra = sorted(got - expected)

    counts = {}
    for k in [PHASE3_TARGET_OBJECT] + [x for x in PHASE3_ALL_OBJECTS if x in spawn_params]:
        counts[k] = counts.get(k, 0) + 1

    dup = sorted([k for k, v in counts.items() if v > 1])

    print("[SPAWN SET CHECK] target=", PHASE3_TARGET_OBJECT)
    print("[SPAWN SET CHECK] expected=", PHASE3_ALL_OBJECTS)
    print("[SPAWN SET CHECK] actual=", sorted(got))
    print("[SPAWN SET CHECK] missing=", missing, "duplicate=", dup, "extra=", extra)

    if missing or dup or extra:
        raise RuntimeError(f"BAD SPAWN SET: missing={missing} duplicate={dup} extra={extra}")

    return True

def phase3_apply_semantic_labels(stage, verbose=False):
    # Disabled at runtime. Semantic labels are stored in USD asset files.
    return

def phase3_warmup_semantic_render(env, n=10):
    return

def phase3_warmup_semantic_render(env, n=10):
    return

def phase3_warmup_semantic_render(env, n=10):
    return

def phase3_warmup_semantic_render(env, n=10):
    try:
        import omni.usd
        stage = omni.usd.get_context().get_stage()
    except Exception:
        pass

    try:
        for _ in range(int(n)):
            env.sim.render()
    except Exception:
        pass

def phase3_warmup_semantic_render(env, n=8):
    """
    Give Replicator/semantic annotator a few frames after semantic labels are applied.
    """
    try:
        import omni.usd
        stage = omni.usd.get_context().get_stage()
    except Exception:
        pass

    try:
        for _ in range(int(n)):
            env.sim.render()
    except Exception:
        try:
            for _ in range(int(n)):
                env.step(env.action_manager.action)
        except Exception:
            pass

def phase3_hide_all_debug_visuals(stage, verbose=False):
    """
    Dataset-safe visual cleanup.
    IMPORTANT: never RemovePrim() during runtime because PhysX tensor views become invalid.
    Only MakeInvisible() debug render prims.
    """
    if RECORD_DEBUG_VISUALS:
        return

    try:
        from pxr import UsdGeom
    except Exception:
        return

    BAD_TOKENS = [
        "phase3spawngrid",
        "phase3grid",
        "spawngrid",
        "gridvisual",
        "grid_visual",
        "gridline",
        "grid_line",
        "gridlines",
        "grid_lines",
        "gridmarker",
        "grid_marker",
        "gridsphere",
        "grid_sphere",
        "gridcube",
        "grid_cube",
        "activecell",
        "active_cell",
        "cellmarker",
        "cell_marker",
        "targetmarker",
        "target_marker",
        "targetsquare",
        "target_square",
        "redsquare",
        "red_square",
        "waypoint",
        "waypointmarker",
        "waypoint_marker",
        "debugmarker",
        "debug_marker",
        "visualmarker",
        "visual_marker",
        "phase3marker",
        "phase3_marker",
        "griddirection",
        "grid_direction",
        "calibration",
        "hover_marker",
        "grasp_marker",
        "lift_marker",
        "place_marker",
        "retreat_marker",
        "centroid_marker",
        "root_origin_debug_red",
        "debug_red",
    ]

    hidden = []

    def is_red_display_color(prim):
        try:
            gp = UsdGeom.Gprim(prim)
            if not gp:
                return False
            attr = gp.GetDisplayColorAttr()
            val = attr.Get() if attr else None
            if not val:
                return False
            c = val[0]
            r, g, b = float(c[0]), float(c[1]), float(c[2])
            return r > 0.35 and g < 0.30 and b < 0.30
        except Exception:
            return False

    for prim in stage.Traverse():
        try:
            p = str(prim.GetPath())
            pl = p.lower()

            hit = any(tok in pl for tok in BAD_TOKENS) or is_red_display_color(prim)
            if not hit:
                continue

            img = UsdGeom.Imageable(prim)
            if img:
                img.MakeInvisible()
                hidden.append(p)

        except Exception:
            pass

    try:
        from omni.isaac.debug_draw import _debug_draw
        draw = _debug_draw.acquire_debug_draw_interface()
        try:
            draw.clear_points()
        except Exception:
            pass
        try:
            draw.clear_lines()
        except Exception:
            pass
    except Exception:
        pass

    if verbose and hidden:
        print("[PHASE3 VIS HIDE SAFE] hidden=", len(hidden))
        for p in hidden[:40]:
            print("  HIDE", p)
        if len(hidden) > 40:
            print("  ...", len(hidden)-40, "more")

def draw_spawn_grid_debug(*args, **kwargs):
    return None

def draw_spawn_grid_usd(*args, **kwargs):
    return None

def draw_grid_direction_calibration(*args, **kwargs):
    return None

def draw_target_marker(*args, **kwargs):
    return None

def draw_target_marker_usd(*args, **kwargs):
    return None

def draw_waypoint_markers(*args, **kwargs):
    return None

def draw_waypoint_markers_usd(*args, **kwargs):
    return None

def hide_phase3_visual_prims(stage):
    """
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    Hide all renderable debug/grid/target prims so RGB cameras won't record them.
    """
    try:
        from pxr import UsdGeom
    except Exception as e:
        print("[VIS HIDE IMPORT WARN]", e)
        return

    BAD_TOKENS = [
        "phase3spawngrid",
        "griddirection",
        "griddirectioncalibration",
        "spawngrid",
        "gridmarker",
        "waypoint",
        "targetmarker",
        "visualmarker",
        "debugmarker",
        "redsquare",
        "targetsquare",
        "activecell",
        "gridcube",
        "gridsphere",
        "grid_box",
        "gridbox",
        "marker",
        "calibration",
        "fof_mesh_magenta_box",
    ]

    hidden = []
    for prim in stage.Traverse():
        try:
            p = str(prim.GetPath())
            pl = p.lower()
            if any(tok in pl for tok in BAD_TOKENS):
                img = UsdGeom.Imageable(prim)
                if img:
                    img.MakeInvisible()
                    hidden.append(p)
        except Exception:
            pass

    if hidden:
        print("[VIS HIDE] hidden prims:")
        for p in hidden:
            print("   ", p)

def draw_spawn_grid_debug(*args, **kwargs):
    return None

def draw_spawn_grid_usd(*args, **kwargs):
    return None

def draw_grid_direction_calibration(*args, **kwargs):
    return None

def draw_target_marker(*args, **kwargs):
    return None

def draw_target_marker_usd(*args, **kwargs):
    return None

def draw_waypoint_markers(*args, **kwargs):
    return None

def draw_waypoint_markers_usd(*args, **kwargs):
    return None

def _get_or_create_marker(stage, prim_path, radius, rgba):
    prim = stage.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        sphere = UsdGeom.Sphere.Define(stage, prim_path)
        sphere.GetRadiusAttr().Set(radius)
        sphere.GetDisplayColorAttr().Set([(rgba[0], rgba[1], rgba[2])])
        sphere.GetDisplayOpacityAttr().Set([rgba[3]])
        prim = sphere.GetPrim()
        prim.SetInstanceable(False)
        UsdGeom.Imageable(prim).MakeInvisible()
        _marker_registry[prim_path] = sphere
    return _marker_registry.get(prim_path, UsdGeom.Sphere(stage.GetPrimAtPath(prim_path)))

def show_marker(stage, prim_path, pos, marker_type="default"):
    if not SHOW_MARKERS: return
    rgba = MARKER_COLORS.get(marker_type,(1,1,1,1))
    radius = MARKER_RADIUS.get(marker_type,MARKER_RADIUS["default"])
    sphere = _get_or_create_marker(stage, prim_path, radius, rgba)
    if hasattr(pos,"tolist"): pos = pos.tolist()
    xform = UsdGeom.Xformable(sphere.GetPrim())
    ops = xform.GetOrderedXformOps()
    t_op = next((o for o in ops if o.GetOpType()==UsdGeom.XformOp.TypeTranslate),None)
    if t_op is None:
        xform.ClearXformOpOrder(); t_op = xform.AddTranslateOp()
    t_op.Set(Gf.Vec3d(float(pos[0]),float(pos[1]),float(pos[2])))
    UsdGeom.Imageable(sphere.GetPrim()).MakeVisible()

def hide_all_markers(stage):
    if not SHOW_MARKERS: return
    for _,sphere in _marker_registry.items():
        try: UsdGeom.Imageable(sphere.GetPrim()).MakeInvisible()
        except: pass

def place_waypoint_markers(stage, obj_name, waypoints):
    if not SHOW_MARKERS: return
    prefix = f"/World/Markers/{obj_name}"
    for label, pos in waypoints.items():
        show_marker(stage, f"{prefix}/{label}", pos, label if label in MARKER_COLORS else "default")


# =============================================================================
# Frame / sensor helpers (identical to ok_dual_1)
# =============================================================================

def to_base_pos(env, pos_w):
    robot = env.scene["robot"]
    return quat_apply(quat_inv(robot.data.root_quat_w[0:1]),
                      pos_w.reshape(1,3) - robot.data.root_pos_w[0:1])[0]

def to_base_quat(env, quat_w):
    robot = env.scene["robot"]
    return quat_mul(quat_inv(robot.data.root_quat_w[0:1]), quat_w.reshape(1,4))[0]

def get_ee_pos_w(env):
    ee = env.scene["ee_frame"]; ee.update(dt=env.physics_dt)
    return ee.data.target_pos_w[0,0].clone()

def get_ee_quat_w(env):
    ee = env.scene["ee_frame"]; ee.update(dt=env.physics_dt)
    return ee.data.target_quat_w[0,0].clone()

def get_scalpel_type2_pos_w(env):  return env.scene["object"].data.root_pos_w[0].clone()
def get_scalpel_type2_quat_w(env): return env.scene["object"].data.root_quat_w[0].clone()
def get_scalpel_pos_w(env):  return env.scene["scalpel"].data.root_pos_w[0].clone()
def get_scalpel_quat_w(env): return env.scene["scalpel"].data.root_quat_w[0].clone()
def get_obj_vel_w(env, name):
    return torch.linalg.norm(env.scene[phase3_scene_key_for_object(name)].data.root_lin_vel_w[0]).item()


# =============================================================================
# Settle (identical to ok_dual_1)
# =============================================================================

def wait_for_settle(env):
    ee_pos_w  = get_ee_pos_w(env)
    ee_quat_w = get_ee_quat_w(env)
    hold_act  = torch.zeros((env.num_envs, ACTION_DIM), device=env.device)
    hold_act[:,0:3] = to_base_pos(env, ee_pos_w)
    hold_act[:,3:7] = to_base_quat(env, ee_quat_w)
    hold_act[:,7]   = 1.0
    consec = 0
    for step in range(SETTLE_STEPS + SETTLE_CONSEC_OK * SETTLE_POLL_EVERY):
        env.step(hold_act)
        if step < SETTLE_STEPS: continue
        if step % SETTLE_POLL_EVERY == 0:
            sc_vel = get_obj_vel_w(env,"object")
            sp_vel = get_obj_vel_w(env,"scalpel")
            if sc_vel < SETTLE_VEL_THRESH and sp_vel < SETTLE_VEL_THRESH:
                consec += 1
                if consec >= SETTLE_CONSEC_OK:
                    print(f"[SETTLE] at rest after {step} steps (sc={sc_vel:.4f} sp={sp_vel:.4f})")
                    return
            else:
                consec = 0
    print("[SETTLE] max steps reached ??proceeding")


# =============================================================================
# State / slerp / actions (identical to ok_dual_1)
# =============================================================================


phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
def _camera_rgb_uint8_strict(cam):
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    """Read real RGB from IsaacLab Camera output['rgb'] only."""
    import numpy as _np

    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    out = cam.data.output
    if "rgb" not in out:
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        raise RuntimeError(f"Camera has no rgb output. Available keys: {list(out.keys())}")

    x = out["rgb"]
    if hasattr(x, "detach"):
        x = x[0].detach().cpu().numpy()
    else:
        x = x[0]

    x = _np.asarray(x)

    if x.ndim == 3 and x.shape[-1] == 4:
        x = x[..., :3]

    if x.dtype != _np.uint8:
        if x.max() <= 1.5:
            x = _np.clip(x * 255.0, 0, 255)
        else:
            x = _np.clip(x, 0, 255)
        x = x.astype(_np.uint8)

    return x


def _camera_depth_float16_strict(cam):
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    """Read real depth from IsaacLab Camera output['distance_to_image_plane'] only."""
    import numpy as _np

    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    out = cam.data.output
    key = "distance_to_image_plane"
    if key not in out:
        raise RuntimeError(f"Camera has no {key} output. Available keys: {list(out.keys())}")

    x = out[key]
    if hasattr(x, "detach"):
        x = x[0].detach().cpu().numpy()
    else:
        x = x[0]

    x = _np.asarray(x)

    if x.ndim == 3 and x.shape[-1] == 1:
        x = x[..., 0]

    return x.astype(_np.float16)


def make_state(env, active_target_w, phase_id):
    robot = env.scene["robot"]
    st = torch.cat([
        robot.data.joint_pos[0],
        to_base_pos(env,  get_ee_pos_w(env)),
        to_base_quat(env, get_ee_quat_w(env)),
        to_base_pos(env,  get_scalpel_type2_pos_w(env)),
        to_base_quat(env, get_scalpel_type2_quat_w(env)),
        to_base_pos(env,  get_scalpel_pos_w(env)),
        to_base_quat(env, get_scalpel_quat_w(env)),
        to_base_pos(env,  active_target_w),
        torch.tensor([float(phase_id)], device=env.device),
    ], dim=0)
    assert st.shape[0] == STATE_DIM
    return st

def slerp(q0, q1, t):
    q0 = q0/(torch.linalg.norm(q0)+1e-9)
    q1 = q1/(torch.linalg.norm(q1)+1e-9)
    dot = torch.clamp(torch.dot(q0,q1),-1.0,1.0)
    if dot < 0.0: q1=-q1; dot=-dot
    if dot > SLERP_FALLBACK_DOT:
        return torch.nn.functional.normalize(q0+t*(q1-q0),dim=0)
    th0=torch.acos(dot); th=th0*t; s0=torch.sin(th0)
    return (torch.sin(th0-th)/s0)*q0+(torch.sin(th)/s0)*q1

def make_abs_action(env, target_w, quat_w, grip):
    a = torch.zeros((env.num_envs,ACTION_DIM),device=env.device)
    a[:,0:3]=to_base_pos(env,target_w)
    a[:,3:7]=to_base_quat(env,quat_w)
    a[:,7]=grip
    return a

def make_dp_action(env, target_w, quat_w, grip):
    return make_abs_action(env,target_w,quat_w,grip)


# =============================================================================
# Camera helpers
# =============================================================================

def _to_uint8_rgb(x):
    if isinstance(x, torch.Tensor):
        x = x.detach().cpu().numpy()
    else:
        x = np.asarray(x)

    x = x[:, :, :3]

    if x.dtype != np.uint8:
        if x.max() <= 1.5:
            x = (x * 255.0).clip(0, 255).astype(np.uint8)
        else:
            x = x.clip(0, 255).astype(np.uint8)

    return x

def _to_float16_depth(x, height=CAMERA_HEIGHT, width=CAMERA_WIDTH):
    if x is None:
        return np.zeros((height, width), dtype=np.float16)

    if isinstance(x, torch.Tensor):
        x = x.detach().cpu().numpy()
    else:
        x = np.asarray(x)

    if x.ndim == 3 and x.shape[-1] == 1:
        x = x[:, :, 0]

    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    return x.astype(np.float16)

def _rotate_grip_b_if_needed(rgb, depth):
    if GRIP_B_ROT90_K is None or int(GRIP_B_ROT90_K) % 4 == 0:
        return rgb, depth

    k = int(GRIP_B_ROT90_K) % 4
    rgb = np.rot90(rgb, k=k).copy()
    depth = np.rot90(depth, k=k).copy()
    return rgb, depth

phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
def read_camera_rgb_depth(env, cam_name, rotate_grip_b=False):
    cam = env.scene[cam_name]
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    out = cam.data.output

    rgb = _to_uint8_rgb(out["rgb"][0])

    depth_raw = out.get("distance_to_image_plane", None)
    depth = _to_float16_depth(
        depth_raw[0] if depth_raw is not None else None,
        rgb.shape[0],
        rgb.shape[1],
    )

    if rotate_grip_b:
        rgb, depth = _rotate_grip_b_if_needed(rgb, depth)

    return rgb, depth

def _safe_name(x):
    return str(x).replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "_")

def _depth_to_vis_uint8(depth):
    d = np.asarray(depth, dtype=np.float32)
    d = np.nan_to_num(d, nan=0.0, posinf=0.0, neginf=0.0)

    valid = d[d > 1e-6]
    if valid.size == 0:
        return np.zeros(d.shape, dtype=np.uint8)

    lo = float(np.percentile(valid, 2.0))
    hi = float(np.percentile(valid, 98.0))

    if hi <= lo + 1e-9:
        hi = lo + 1e-6

    # Invert: closer = brighter.
    vis = 1.0 - np.clip((d - lo) / (hi - lo), 0.0, 1.0)
    return (vis * 255.0).astype(np.uint8)

def _select_export_indices(stage_names, total_steps, stride=50, export_all=False):
    if total_steps <= 0:
        return []

    if export_all:
        return list(range(total_steps))

    idxs = {0, total_steps - 1}

    prev = None
    for i, st in enumerate(stage_names):
        if st != prev:
            idxs.add(i)
            prev = st

    for i in range(0, total_steps, max(1, stride)):
        idxs.add(i)

    return sorted(idxs)


# =============================================================================
# Step executors (identical to ok_dual_1)
# =============================================================================

def step_dynamic(env, recorder, name, target_w, quat_w, grip,
                 active_target_w, phase_id,
                 max_steps=80, dist_thresh=0.015, settle_steps=6, force_wait=False):
    start_pos  = get_ee_pos_w(env).clone()
    start_quat = get_ee_quat_w(env).clone()
    timer=0; max_z=-999.0
    for i in range(max_steps):
        t = min(1.0,(i+1)/max(MIN_INTERP_STEPS,1))
        ip = start_pos + t*(target_w-start_pos)
        iq = slerp(start_quat,quat_w,t)
        st = make_state(env,active_target_w,phase_id)
        a  = make_abs_action(env,ip,iq,grip)
        recorder.add_step(env,name,i,st,a)
        env.step(a)
        ee=get_ee_pos_w(env)
        dist=torch.linalg.norm((ee-target_w)[:3]).item()
        # track active object z
        obj = get_scalpel_pos_w(env) if phase_id==0 else get_scalpel_type2_pos_w(env)
        max_z=max(max_z,float(obj[2]))
        if i==0 or i%args_cli.debug_every==0:
            print(f"[{name}] i={i:04d} dist={dist:.4f} obj_z={float(obj[2]):.4f} ee_z={float(ee[2]):.4f} g={grip:.2f}")
        if not force_wait and i>=MIN_INTERP_STEPS and dist<dist_thresh:
            timer+=1
            if timer>=settle_steps:
                print(f"[{name}] reached i={i}"); break
        else:
            timer=0
    return max_z

def step_smooth_grip(env, recorder, name, target_w, quat_w,
                     grip_start, grip_end, tray_slot_w, phase_id, steps=40):
    max_z=-999.0; hold=abs(grip_start-grip_end)<0.01
    for i in range(steps):
        if hold:
            grip=grip_start
        else:
            t=max(0.0,(i-steps//4))/max(steps-steps//4-1,1)
            grip=grip_start+min(1.0,t)*(grip_end-grip_start)
        st=make_state(env,tray_slot_w,phase_id)
        a =make_abs_action(env,target_w,quat_w,grip)
        recorder.add_step(env,name,i,st,a)
        env.step(a)
        obj=get_scalpel_pos_w(env) if phase_id==0 else get_scalpel_type2_pos_w(env)
        max_z=max(max_z,float(obj[2]))
        if i==0 or i%args_cli.debug_every==0:
            ee=get_ee_pos_w(env)
            print(f"[{name}] i={i:03d} grip={grip:.3f} obj_z={float(obj[2]):.4f} ee_z={float(ee[2]):.4f}")
    return max_z

def step_hold_const_grip(env, recorder, name, target_w, quat_w,
                         grip, tray_slot_w, phase_id, steps=80):
    """Hold EE fixed with a constant gripper command.

    Use this for scalpel_type2 close: no delayed ramp, so the fingers clamp before lift.
    """
    max_z = -999.0
    for i in range(steps):
        st = make_state(env, tray_slot_w, phase_id)
        a  = make_abs_action(env, target_w, quat_w, grip)
        recorder.add_step(env, name, i, st, a)
        env.step(a)

        obj = get_scalpel_pos_w(env) if phase_id == 0 else get_scalpel_type2_pos_w(env)
        max_z = max(max_z, float(obj[2]))

        if i == 0 or i % args_cli.debug_every == 0:
            ee = get_ee_pos_w(env)
            print(f"[{name}] i={i:03d} grip={grip:.3f} obj_z={float(obj[2]):.4f} ee_z={float(ee[2]):.4f}")
    return max_z


# =============================================================================
# Recorder: front camera + selected grip_b camera
# =============================================================================

class EpisodeRecorder:
    def __init__(self, output_dir, task_description, debug_every=25):
        self.output_dir = output_dir
        self.task_description = task_description
        self.debug_every = debug_every

        os.makedirs(output_dir, exist_ok=True)
        self._reset()

    def _reset(self):
        self.states = []
        self.actions = []
        self.stage_names = []
        self.step_ids = []

        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        self.front_rgb = []
        self.front_depth = []
        self.front_semantic = []

        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        self.grip_b_rgb = []
        self.grip_b_depth = []
        self.grip_b_semantic = []

        # Backward-compatible aliases.
        self.images = []          # observations/images = front RGB
        self.images_front = []
        self.images_wrist = []    # observations/images_wrist = grip_b RGB
        self.depth_front = []
        self.depth_wrist = []
        self.extra_camera_rgb = {name: [] for name in PHASE3_EXTRA_CAMERA_NAMES}
        self.extra_camera_depth = {name: [] for name in PHASE3_EXTRA_CAMERA_NAMES}
        self.extra_camera_semantic = {name: [] for name in PHASE3_EXTRA_CAMERA_NAMES}
     # observations/depth_wrist = grip_b depth

    def add_step(self, env, stage_name, step_id, state, action):
        front_rgb = front_depth = front_semantic = grip_rgb = grip_depth = grip_b_semantic = None
        extra_camera_payload = {}

        try:
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            front_rgb, front_depth = read_camera_rgb_depth(env, "camera", rotate_grip_b=False)
            front_semantic = _phase3_extract_semantic_u16(env.scene["camera"], CAMERA_HEIGHT, CAMERA_WIDTH, cam_name="front")
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            grip_rgb, grip_depth = read_camera_rgb_depth(env, "grip_cam_b", rotate_grip_b=False)
            grip_b_semantic = _phase3_extract_semantic_u16(env.scene["grip_cam_b"], CAMERA_HEIGHT, CAMERA_WIDTH, cam_name="grip_b")
            # [PHASE3 EXTRA CAMERA READ]
            _scene_keys = set(list(env.scene.keys()))
            for _cam_name in PHASE3_EXTRA_CAMERA_NAMES:
                if _cam_name not in _scene_keys:
                    continue
                _rgb, _depth = read_camera_rgb_depth(env, _cam_name, rotate_grip_b=False)
                _sem = phase3_safe_semantic(env.scene[_cam_name], CAMERA_HEIGHT, CAMERA_WIDTH, _cam_name, _phase3_extract_semantic_u16)
                extra_camera_payload[_cam_name] = (_rgb, _depth, _sem)

        except Exception as e:
            if not self.actions:
                phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
                print("[CAMERA ERROR]", repr(e))

        self.states.append(state.detach().cpu().numpy().astype(np.float32))
        self.actions.append(action[0].detach().cpu().numpy().astype(np.float32))
        self.stage_names.append(stage_name)
        self.step_ids.append(step_id)

        if front_rgb is not None:
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            self.front_rgb.append(front_rgb)
            self.front_depth.append(front_depth)
            self.front_semantic.append(front_semantic)

            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            self.images.append(front_rgb)
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            self.images_front.append(front_rgb)
            self.depth_front.append(front_depth)

        if grip_rgb is not None:
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            self.grip_b_rgb.append(grip_rgb)
            self.grip_b_depth.append(grip_depth)
            self.grip_b_semantic.append(grip_b_semantic)

            self.images_wrist.append(grip_rgb)
            self.depth_wrist.append(grip_depth)


        # [PHASE3 EXTRA CAMERA APPEND]
        if front_rgb is not None:
            _zero_rgb = np.zeros_like(front_rgb, dtype=np.uint8)
            _zero_depth = np.zeros_like(front_depth, dtype=np.float16)
            _zero_sem = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH), dtype=np.uint16)
            for _cam_name in PHASE3_EXTRA_CAMERA_NAMES:
                _payload = extra_camera_payload.get(_cam_name)
                if _payload is None:
                    self.extra_camera_rgb[_cam_name].append(_zero_rgb)
                    self.extra_camera_depth[_cam_name].append(_zero_depth)
                    self.extra_camera_semantic[_cam_name].append(_zero_sem)
                else:
                    _rgb, _depth, _sem = _payload
                    self.extra_camera_rgb[_cam_name].append(_rgb)
                    self.extra_camera_depth[_cam_name].append(_depth)
                    self.extra_camera_semantic[_cam_name].append(_sem)

        n = len(self.actions)
        if n == 1 or n % self.debug_every == 0:
            print(f"[REC step={n:04d}] stage={stage_name}")

    def _export_preview_folders(self, ep_idx):
        T = len(self.actions)

        base_dir = os.path.join(self.output_dir, f"episode_{ep_idx:06d}_preview")
        os.makedirs(base_dir, exist_ok=True)

        front_rgb_dir = os.path.join(base_dir, "front_rgb")
        front_depth_dir = os.path.join(base_dir, "front_depth")
        grip_rgb_dir = os.path.join(base_dir, "grip_b_rgb")
        grip_depth_dir = os.path.join(base_dir, "grip_b_depth")

        os.makedirs(front_rgb_dir, exist_ok=True)
        os.makedirs(front_depth_dir, exist_ok=True)
        os.makedirs(grip_rgb_dir, exist_ok=True)
        os.makedirs(grip_depth_dir, exist_ok=True)

        indices = _select_export_indices(
            self.stage_names,
            T,
            stride=CAMERA_EXPORT_STRIDE,
            export_all=EXPORT_ALL_PNG_STEPS,
        )

        for sidx in indices:
            stage = _safe_name(self.stage_names[sidx])

            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            Image.fromarray(self.front_rgb[sidx]).save(
                os.path.join(front_rgb_dir, f"step_{sidx:04d}_{stage}.png")
            )
            Image.fromarray(_depth_to_vis_uint8(self.front_depth[sidx])).save(
                os.path.join(front_depth_dir, f"step_{sidx:04d}_{stage}.png")
            )

            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            Image.fromarray(self.grip_b_rgb[sidx]).save(
                os.path.join(grip_rgb_dir, f"step_{sidx:04d}_{stage}.png")
            )
            Image.fromarray(_depth_to_vis_uint8(self.grip_b_depth[sidx])).save(
                os.path.join(grip_depth_dir, f"step_{sidx:04d}_{stage}.png")
            )

        info_path = os.path.join(base_dir, "preview_info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"episode={ep_idx}\n")
            f.write(f"num_steps={T}\n")
            f.write(f"export_stride={CAMERA_EXPORT_STRIDE}\n")
            f.write(f"export_all_steps={EXPORT_ALL_PNG_STEPS}\n")
            f.write(f"grip_b_rot90_k={GRIP_B_ROT90_K}\n")
            f.write("views=front, grip_b, cam_top, cam_left, cam_right, cam_tray\n\n")
            f.write("folder layout:\n")
            f.write("  front_rgb\n")
            f.write("  front_depth\n")
            f.write("  grip_b_rgb\n")
            f.write("  grip_b_depth\n\n")
            f.write("selected steps:\n")
            for sidx in indices:
                f.write(f"  {sidx:04d}  {self.stage_names[sidx]}\n")

        print(f"[Preview Export] {base_dir}")

    def save_episode(self, ep_idx, success, meta=None):
        if not self.actions:
            self._reset()
            return False

        if not success:
            self._reset()
            return False

        T = len(self.actions)

        if (
            len(self.front_rgb) != T or
            len(self.front_depth) != T or
            len(self.grip_b_rgb) != T or
            len(self.grip_b_depth) != T
        ):
            print(
                "[Recorder] image/depth length mismatch:",
                f"T={T}",
                f"front_rgb={len(self.front_rgb)}",
                f"front_depth={len(self.front_depth)}",
                f"grip_b_rgb={len(self.grip_b_rgb)}",
                f"grip_b_depth={len(self.grip_b_depth)}",
            )
            self._reset()
            return False

        states = np.asarray(self.states, dtype=np.float32)
        actions = np.asarray(self.actions, dtype=np.float32)

        front_rgb = np.asarray(self.front_rgb, dtype=np.uint8)
        front_depth = np.asarray(self.front_depth, dtype=np.float16)

        grip_b_rgb = np.asarray(self.grip_b_rgb, dtype=np.uint8)
        grip_b_depth = np.asarray(self.grip_b_depth, dtype=np.float16)

        dones = np.zeros((T,), dtype=np.bool_)
        dones[-1] = True

        path = os.path.join(self.output_dir, f"episode_{ep_idx:06d}.h5")

        with h5py.File(path, "w") as f:
            f.attrs["language_instruction"] = self.task_description
            f.attrs["task_description"] = self.task_description
            f.attrs["success"] = bool(success)
            f.attrs["num_samples"] = int(T)
            f.attrs["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.attrs["state_dim"] = STATE_DIM
            f.attrs["action_dim"] = ACTION_DIM
            f.attrs["action_type"] = "absolute_pose_quat_gripper_8d_baseframe"
            f.attrs["state_frame"] = "robot_base"
            f.attrs["action_frame"] = "robot_base"
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            f.attrs["camera_views"] = json.dumps(list(PHASE3_ALL_CAMERA_VIEWS))

            f.attrs["semantic_mapping_version"] = "phase3_canonical_v1"
            f.attrs["semantic_class_ids"] = json.dumps({
                "background": 0,
                "robot": 1,
                "surgical_tray": 2,
                "scalpel": 3,
                "scissor": 4,
                "love_retractor": 5,
                "kelly": 6,
                "scalpel_type2": 7,
            })
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            f.attrs["camera_rgb_shape"] = json.dumps([CAMERA_HEIGHT, CAMERA_WIDTH, 3])
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            f.attrs["camera_depth_shape"] = json.dumps([CAMERA_HEIGHT, CAMERA_WIDTH])
            f.attrs["depth_type"] = "distance_to_image_plane_meters_float16"
            phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
            f.attrs["grip_b_camera_prim"] = GRIP_B_CAMERA_PRIM
            f.attrs["grip_b_pos"] = json.dumps(list(GRIP_B_POS))
            f.attrs["grip_b_rot"] = json.dumps(list(GRIP_B_ROT))
            f.attrs["grip_b_rot90_k"] = int(GRIP_B_ROT90_K)
            f.attrs["state_keys"] = json.dumps(STATE_KEYS)
            f.attrs["action_keys"] = json.dumps(ACTION_KEYS)
            f.attrs["pick_order"] = "scalpel_type2_only"
            f.attrs["task_mode"] = "scalpel_type2_only"
            f.attrs["scalpel_slot"] = "right"
            f.attrs["scalpel_type2_slot"] = "left"
            f.attrs["scalpel_local_center_x"] = SCALPEL_LOCAL_CENTER[0]
            f.attrs["scalpel_local_center_y"] = SCALPEL_LOCAL_CENTER[1]
            f.attrs["scalpel_local_center_z"] = SCALPEL_LOCAL_CENTER[2]
            f.attrs["offset_model"] = "verified_local_center_quat_apply_direct_spawn"

            if meta:
                for k, v in meta.items():
                    try:
                        f.attrs[k] = v
                    except Exception:
                        f.attrs[k] = str(v)

            obs = f.create_group("observations")

            obs.create_dataset("state", data=states)
            obs.create_dataset("proprio", data=states)

            # Backward compatibility.
            obs.create_dataset("images", data=front_rgb, compression="gzip")
            obs.create_dataset("images_front", data=front_rgb, compression="gzip")
            obs.create_dataset("depth_front", data=front_depth, compression="gzip")

            # Backward compatibility for old wrist naming.
            obs.create_dataset("images_wrist", data=grip_b_rgb, compression="gzip")
            obs.create_dataset("depth_wrist", data=grip_b_depth, compression="gzip")

            # Explicit final gripper camera naming.
            obs.create_dataset("images_grip_b", data=grip_b_rgb, compression="gzip")
            obs.create_dataset("depth_grip_b", data=grip_b_depth, compression="gzip")

            f.create_dataset("actions", data=actions)
            f.create_dataset("dones", data=dones)
            f.create_dataset("rewards", data=np.zeros((T,), dtype=np.float32))
            f.create_dataset("stage_names", data=np.asarray(self.stage_names, dtype=h5py.string_dtype()))
            f.create_dataset("step_ids", data=np.asarray(self.step_ids, dtype=np.int32))

            ns = f.create_group("norm_stats")
            ns.create_dataset("state_mean", data=states.mean(0).astype(np.float32))
            ns.create_dataset("state_std", data=(states.std(0) + 1e-8).astype(np.float32))
            ns.create_dataset("action_mean", data=actions.mean(0).astype(np.float32))
            ns.create_dataset("action_std", data=(actions.std(0) + 1e-8).astype(np.float32))

        self._export_preview_folders(ep_idx)

        print(f"[Recorder] Saved episode {ep_idx} | steps={T} | path={path}")
        self._reset()
        return True

# =============================================================================
# Yaw helpers (identical to ok_dual_1 ??used for gripper orientation only)
# =============================================================================

def yaw_from_quat_wxyz(q):
    w,x,y,z=q[0],q[1],q[2],q[3]
    return torch.atan2(2.0*(w*z+x*y),1.0-2.0*(y*y+z*z))

def yaw_quat_wxyz(yaw, device):
    return torch.tensor([torch.cos(yaw/2).item(),0.0,0.0,torch.sin(yaw/2).item()],device=device)


# =============================================================================
# Tray (identical to ok_dual_1)
# =============================================================================

def spawn_tray(stage, tray_pos):
    path="/World/RandomTray"
    old=stage.GetPrimAtPath(path)
    if old.IsValid(): stage.RemovePrim(path)
    tray=UsdGeom.Xform.Define(stage,path)
    tray.GetPrim().GetReferences().AddReference(TRAY_USD,"/Root/SurgicalTray")
    tray.ClearXformOpOrder()
    tray.AddTranslateOp().Set(Gf.Vec3d(float(tray_pos[0]),float(tray_pos[1]),0.006))
    tray.AddScaleOp().Set(Gf.Vec3d(0.0025,0.0025,0.0025))
    print("[TRAY] center=",[round(float(tray_pos[0]),4),round(float(tray_pos[1]),4),0.006])


# =============================================================================
# Direct spawn + scalpel pose helpers
# =============================================================================

def quat_from_rotmat_wxyz(R, device):
    # R columns = local X/Y/Z axes expressed in world frame. Return wxyz.
    m00, m01, m02 = R[0,0], R[0,1], R[0,2]
    m10, m11, m12 = R[1,0], R[1,1], R[1,2]
    m20, m21, m22 = R[2,0], R[2,1], R[2,2]
    tr = m00 + m11 + m22
    if float(tr) > 0.0:
        S = torch.sqrt(tr + 1.0) * 2.0
        qw = 0.25 * S
        qx = (m21 - m12) / S
        qy = (m02 - m20) / S
        qz = (m10 - m01) / S
    elif float(m00) > float(m11) and float(m00) > float(m22):
        S = torch.sqrt(1.0 + m00 - m11 - m22) * 2.0
        qw = (m21 - m12) / S
        qx = 0.25 * S
        qy = (m01 + m10) / S
        qz = (m02 + m20) / S
    elif float(m11) > float(m22):
        S = torch.sqrt(1.0 + m11 - m00 - m22) * 2.0
        qw = (m02 - m20) / S
        qx = (m01 + m10) / S
        qy = 0.25 * S
        qz = (m12 + m21) / S
    else:
        S = torch.sqrt(1.0 + m22 - m00 - m11) * 2.0
        qw = (m10 - m01) / S
        qx = (m02 + m20) / S
        qy = (m12 + m21) / S
        qz = 0.25 * S
    q = torch.stack([qw, qx, qy, qz]).to(device)
    return q / (torch.linalg.norm(q) + 1e-9)

def make_scalpel_broad_flat_quat(yaw_rad, device):
    # Verified flat pose for knife_centered.usd:
    # local +Y points downward, so root can be high while body center is on table.
    c = torch.cos(torch.tensor(yaw_rad, device=device))
    s = torch.sin(torch.tensor(yaw_rad, device=device))
    world_y = torch.tensor([0.0, 0.0, -1.0], device=device)
    world_x = torch.stack([c, s, torch.tensor(0.0, device=device)])
    world_z = torch.cross(world_x, world_y, dim=0)
    world_x = world_x / (torch.linalg.norm(world_x) + 1e-9)
    world_y = world_y / (torch.linalg.norm(world_y) + 1e-9)
    world_z = world_z / (torch.linalg.norm(world_z) + 1e-9)
    R = torch.stack([world_x, world_y, world_z], dim=1)
    return quat_from_rotmat_wxyz(R, device)

def make_scalpel_edge_side_quat(yaw_rad, device):
    # Verified edge/side pose:
    # local X points up; local Y lies in the table plane.
    c = torch.cos(torch.tensor(yaw_rad, device=device))
    s = torch.sin(torch.tensor(yaw_rad, device=device))
    world_x = torch.tensor([0.0, 0.0, 1.0], device=device)
    world_y = torch.stack([c, s, torch.tensor(0.0, device=device)])
    world_z = torch.cross(world_x, world_y, dim=0)
    world_x = world_x / (torch.linalg.norm(world_x) + 1e-9)
    world_y = world_y / (torch.linalg.norm(world_y) + 1e-9)
    world_z = world_z / (torch.linalg.norm(world_z) + 1e-9)
    R = torch.stack([world_x, world_y, world_z], dim=1)
    return quat_from_rotmat_wxyz(R, device)

def choose_scalpel_pose_mode(attempt):
    if not SCALPEL_POSE_SEQUENCE:
        return "BROAD_FLAT"
    return SCALPEL_POSE_SEQUENCE[(attempt - 1) % len(SCALPEL_POSE_SEQUENCE)].upper()

def local_axis_to_world(obj_quat, axis_xyz, device):
    axis = torch.tensor(axis_xyz, device=device, dtype=obj_quat.dtype)
    return quat_apply(obj_quat.reshape(1,4), axis.reshape(1,3))[0]

def local_point_to_world(obj_raw, obj_quat, local_xyz, device):
    local = torch.tensor(local_xyz, device=device, dtype=obj_raw.dtype)
    return obj_raw + quat_apply(obj_quat.reshape(1,4), local.reshape(1,3))[0]

def get_scalpel_center_w(env):
    return local_point_to_world(get_scalpel_pos_w(env), get_scalpel_quat_w(env), SCALPEL_LOCAL_CENTER, env.device)

def root_pos_from_desired_scalpel_center(q, center_xyz, device):
    # Root = desired body-center - rotated local body-center offset.
    local_center = torch.tensor(SCALPEL_LOCAL_CENTER, device=device, dtype=q.dtype)
    world_offset = quat_apply(q.reshape(1,4), local_center.reshape(1,3))[0]
    center = torch.tensor(center_xyz, device=device, dtype=q.dtype)
    return center - world_offset


def grid_cell_center(cell_id):
    total = max(1, GRID_COLS * GRID_ROWS)
    cell_id = int(cell_id) % total
    row = cell_id // GRID_COLS
    col = cell_id % GRID_COLS

    # Actual object spawn grid. Do not use VIS_GRID_* here.
    x0, x1 = GRID_X_RANGE
    y0, y1 = GRID_Y_RANGE
    dx = (x1 - x0) / float(GRID_COLS)
    dy = (y1 - y0) / float(GRID_ROWS)

    x = x0 + (col + 0.5) * dx
    y = y0 + (row + 0.5) * dy
    return x, y, row, col


def draw_spawn_grid_debug(*args, **kwargs):
    return None

def _set_xform_translate_scale(prim, pos, scale):
    xform = UsdGeom.Xformable(prim)
    xform.ClearXformOpOrder()
    xform.AddTranslateOp().Set(Gf.Vec3d(float(pos[0]), float(pos[1]), float(pos[2])))
    xform.AddScaleOp().Set(Gf.Vec3d(float(scale[0]), float(scale[1]), float(scale[2])))

def _make_grid_cube(*args, **kwargs):
    return None

def _make_grid_sphere(*args, **kwargs):
    return None

def draw_spawn_grid_debug(*args, **kwargs):
    return None

def draw_grid_direction_calibration(*args, **kwargs):
    return None

def _xy_from_spawn(obj_name, params):
    if obj_name == "scalpel":
        return float(params["center_x"]), float(params["center_y"])
    return float(params["x"]), float(params["y"])

def _dist_xy(a_name, a_params, b_name, b_params):
    ax, ay = _xy_from_spawn(a_name, a_params)
    bx, by = _xy_from_spawn(b_name, b_params)
    return math.hypot(ax - bx, ay - by)

def _sample_extra_obj_params(rng, obj_name):
    yaw = float(rng.uniform(*RANDOM_YAW_DEG_RANGE))
    if obj_name == "scalpel":
        return {
            "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
            "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
            "yaw_deg": yaw,
        }
    if obj_name == "scalpel_type2":
        # ScalpelType2 uses x/y root, same pick table region.
        xr = globals().get("SCALPEL_TYPE2_RANDOM_X_RANGE", GRID_X_RANGE)
        yr = globals().get("SCALPEL_TYPE2_RANDOM_Y_RANGE", GRID_Y_RANGE)
        return {
            "x": float(rng.uniform(*xr)),
            "y": float(rng.uniform(*yr)),
            "yaw_deg": yaw,
        }

    if obj_name == "love_retractor":
        xr = globals().get("LOVE_RANDOM_X_RANGE", GRID_X_RANGE)
        yr = globals().get("LOVE_RANDOM_Y_RANGE", GRID_Y_RANGE)
        return {
            "x": float(rng.uniform(*xr)),
            "y": float(rng.uniform(*yr)),
            "yaw_deg": yaw,
        }

    # scissor uses x/y root, same pick table region.
    xr = globals().get("SCISSOR_RANDOM_X_RANGE", GRID_X_RANGE)
    yr = globals().get("SCISSOR_RANDOM_Y_RANGE", GRID_Y_RANGE)
    return {
        "x": float(rng.uniform(*xr)),
        "y": float(rng.uniform(*yr)),
        "yaw_deg": yaw,
    }

def ensure_two_distractors(spawn_params, target_object, rng):
    """Ensure spawn_params contains scissor, scalpel, scalpel_type2.

    Existing target + first distractor stay unchanged.
    Missing object is sampled as the second distractor.
    """
    target_object = canonical_object_name(target_object) if "canonical_object_name" in globals() else str(target_object).lower()

    existing = [k for k in ALL_PHASE3_OBJECTS if k in spawn_params]
    missing = [k for k in ALL_PHASE3_OBJECTS if k not in spawn_params]

    for obj_name in missing:
        chosen = None
        for _ in range(SPAWN_MAX_TRIES):
            cand = _sample_extra_obj_params(rng, obj_name)
            ok = True
            for ex in existing:
                if _dist_xy(obj_name, cand, ex, spawn_params[ex]) < SPAWN_MIN_OBJ_OBJ:
                    ok = False
                    break
            if ok:
                chosen = cand
                break

        if chosen is None:
            chosen = _sample_extra_obj_params(rng, obj_name)
            print(f"[EXTRA DISTRACTOR WARN] using last relaxed sample for {obj_name}")

        spawn_params[obj_name] = chosen
        existing.append(obj_name)
        print(f"[EXTRA DISTRACTOR] added {obj_name}: {chosen}")

    if "grid" in spawn_params:
        spawn_params["grid"]["requested_num_distractors"] = 3
        spawn_params["grid"]["actual_num_distractors"] = 3
        spawn_params["grid"]["distractor_objects"] = ",".join([x for x in ALL_PHASE3_OBJECTS if x != target_object])

    return spawn_params

def _write_rigid_pose(env, scene_key, pos_xyz, yaw_deg):
    obj = env.scene[scene_key]
    yaw_rad = float(yaw_deg) * math.pi / 180.0
    q = yaw_quat_wxyz(torch.tensor(yaw_rad, device=env.device), env.device)

    root_pose = torch.zeros((env.num_envs, 7), device=env.device)
    root_pose[:, 0:3] = torch.tensor(pos_xyz, device=env.device, dtype=torch.float32).reshape(1, 3)
    root_pose[:, 3:7] = q.reshape(1, 4)

    root_vel = torch.zeros((env.num_envs, 6), device=env.device)
    obj.write_root_pose_to_sim(root_pose)
    obj.write_root_velocity_to_sim(root_vel)
    obj.update(dt=env.physics_dt)


def debug_print_extra_object_positions(env, tag=""):
    for key in ["object", "scalpel", "scissor", "love_retractor"]:
        if key not in env.scene.keys():
            continue
        try:
            pos = env.scene[key].data.root_pos_w[0].detach().cpu().numpy().tolist()
            print(f"[OBJ POS {tag}] {key}: ({pos[0]:.4f},{pos[1]:.4f},{pos[2]:.4f})")
        except Exception as e:
            print(f"[OBJ POS WARN {tag}] {key}: {repr(e)}")


def debug_print_object_positions(env, tag=""):
    for key in ["object", "scalpel", "scissor", "love_retractor", "scalpel_type2"]:
        if key not in env.scene.keys():
            continue
        try:
            pos = env.scene[key].data.root_pos_w[0].detach().cpu().numpy().tolist()
            print(f"[OBJ POS {tag}] {key}: ({pos[0]:.4f},{pos[1]:.4f},{pos[2]:.4f})")
        except Exception as e:
            print(f"[OBJ POS WARN {tag}] {key}: {repr(e)}")


def force_extra_distractors(env, spawn_params, target_object):
    """Force-pose extra distractor objects if they are configured in env.scene."""
    target_object = canonical_object_name(target_object) if "canonical_object_name" in globals() else str(target_object).lower()

    # scalpel_type2 as extra scene key
    if target_object != "scalpel_type2" and "scalpel_type2" in spawn_params and "scalpel_type2" in env.scene.keys():
        p = spawn_params["scalpel_type2"]
        z = float(globals().get("SCALPEL_TYPE2_SPAWN_ROOT_Z", 0.0010))
        _write_rigid_pose(env, "scalpel_type2", [float(p["x"]), float(p["y"]), z], float(p["yaw_deg"]))
        print(f"[SPAWN EXTRA SCALPEL_TYPE2] root=({p['x']:.4f},{p['y']:.4f},{z:.4f}) yaw={p['yaw_deg']:.1f}")

    # love_retractor as extra distractor
    if target_object != "love_retractor" and "love_retractor" in spawn_params and "love_retractor" in env.scene.keys():
        p = spawn_params["love_retractor"]
        z = float(globals().get("LOVE_SPAWN_ROOT_Z", 0.0010))
        _write_rigid_pose(env, "love_retractor", [float(p["x"]), float(p["y"]), z], float(p["yaw_deg"]))
        print(f"[SPAWN EXTRA LOVE] root=({p['x']:.4f},{p['y']:.4f},{z:.4f}) yaw={p['yaw_deg']:.1f}")

    # scissor as extra scene key
    if target_object != "scissor" and "scissor" in spawn_params and "scissor" in env.scene.keys():
        p = spawn_params["scissor"]
        z = float(globals().get("SCISSOR_SPAWN_ROOT_Z", 0.0025))
        _write_rigid_pose(env, "scissor", [float(p["x"]), float(p["y"]), z], float(p["yaw_deg"]))
        print(f"[SPAWN EXTRA SCISSOR] root=({p['x']:.4f},{p['y']:.4f},{z:.4f}) yaw={p['yaw_deg']:.1f}")

    # scalpel is usually already handled by existing force_episode_objects()


def sample_episode_spawn_grid(rng, attempt, target_object):
    """Place target object on a 2D grid cell; randomize yaw; sample the other object as distractor."""
    target_object = str(target_object).lower()
    cell_id = (int(attempt) - 1) % max(1, GRID_COLS * GRID_ROWS)
    gx, gy, grow, gcol = grid_cell_center(cell_id)

    # Random yaw for both target and distractor.
    target_yaw = float(rng.uniform(*RANDOM_YAW_DEG_RANGE))
    distractor_yaw = float(rng.uniform(*RANDOM_YAW_DEG_RANGE))

    last = None
    for _ in range(SPAWN_MAX_TRIES):
        if target_object == "scalpel":
            sp = {"center_x": float(gx), "center_y": float(gy), "yaw_deg": target_yaw}
            sc = {
                "x": float(rng.uniform(*SCALPEL_TYPE2_RANDOM_X_RANGE)),
                "y": float(rng.uniform(*SCALPEL_TYPE2_RANDOM_Y_RANGE)),
                "yaw_deg": distractor_yaw,
            }
            d = math.hypot(sc["x"] - sp["center_x"], sc["y"] - sp["center_y"])
        else:
            sc = {"x": float(gx), "y": float(gy), "yaw_deg": target_yaw}
            sp = {
                "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
                "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
                "yaw_deg": distractor_yaw,
            }
            d = math.hypot(sc["x"] - sp["center_x"], sc["y"] - sp["center_y"])

        last = {
            "scalpel_type2": sc,
            "scalpel": sp,
            "grid": {
                "cell_id": int(cell_id),
                "row": int(grow),
                "col": int(gcol),
                "x": float(gx),
                "y": float(gy),
                "target_object": target_object,
                "target_yaw_deg": float(target_yaw),
                "requested_num_distractors": int(REQUESTED_NUM_DISTRACTORS),
                "actual_num_distractors": 1,
            },
        }
        if d >= SPAWN_MIN_OBJ_OBJ:
            return last

    print("[GRID SPAWN WARN] could not satisfy object-object distance; using last sample")
    return last

def set_semantic_label(stage, prim_path, label):
    """Best-effort semantic label for Isaac synthetic-data/segmentation workflows."""
    prim = stage.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        return False
    if Semantics is None:
        return False
    try:
        api = Semantics.SemanticsAPI.Apply(prim, "Semantics")
        api.CreateSemanticTypeAttr().Set("class")
        api.CreateSemanticDataAttr().Set(str(label))
        return True
    except Exception as e:
        print(f"[SEMANTIC WARN] {prim_path} label={label} failed: {repr(e)}")
        return False


def label_prims_by_name(stage):
    """
    Apply stable semantic CLASS STRINGS for Phase 3.

    Important:
      - scalpel_type2 must be checked BEFORE scalpel
      - numeric semantic IDs from Isaac are NOT treated as stable class IDs
      - GripCamB camera prim is excluded from robot semantics
    """
    counts = {
        "robot": 0,
        "surgical_tray": 0,
        "scalpel": 0,
        "scissor": 0,
        "love_retractor": 0,
        "kelly": 0,
        "scalpel_type2": 0,
    }

    for prim in stage.Traverse():
        path_raw = str(prim.GetPath())
        path = path_raw.lower()
        name = prim.GetName().lower()

        # Do not label camera prims as robot.
        if "gripcamb_final" in path or "/camera" in path:
            continue

        label = None

        # Order matters.
        if "scalpel_type2" in path or "scalpeltype2" in path:
            label = "scalpel_type2"

        elif "love_retractor" in path or "loveretractor" in path:
            label = "love_retractor"

        elif "kelly" in path:
            label = "kelly"

        elif "scissor" in path:
            label = "scissor"

        elif (
            "randomtray" in path
            or "surgicaltray" in path
            or "surgical_tray" in path
            or name == "tray"
        ):
            label = "surgical_tray"

        elif "scalpel" in path or "knife" in path:
            label = "scalpel"

        elif (
            "/robot" in path
            or "panda_" in path
            or "/panda" in path
            or "franka" in path
        ):
            label = "robot"

        if label is not None:
            if set_semantic_label(stage, path_raw, label):
                counts[label] += 1

    print("[SEMANTIC LABELS]", counts)
    return counts


def make_realcompat_state_from_legacy(states, object_type_id, skill_id):
    """Build policy-safe state: robot proprio + object/skill condition; no target pose."""
    states = np.asarray(states, dtype=np.float32)
    robot_proprio = states[:, 0:16]      # joints, fingers, EE pose
    obj = np.full((states.shape[0], 1), float(object_type_id), dtype=np.float32)
    skill = np.full((states.shape[0], 1), float(skill_id), dtype=np.float32)
    return np.concatenate([robot_proprio, obj, skill], axis=1)

def draw_grid_preview_png(out_path, meta):
    """Save a lightweight 2D grid preview for dataset inspection."""
    W, H = 900, 420
    margin_l, margin_t = 70, 60
    grid_w, grid_h = 640, 280
    img = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)

    # title
    target = str(meta.get("target_object", "object"))
    cell_id = int(meta.get("grid_cell_id", -1))
    row = int(meta.get("grid_row", -1))
    col = int(meta.get("grid_col", -1))
    yaw = float(meta.get("target_yaw_deg", 0.0))
    d.text((margin_l, 18), f"2D Grid Recording | target={target} | cell={cell_id} row={row} col={col} | yaw={yaw:.1f} deg", fill=(0,0,0,255))

    # grid
    x0, y0 = margin_l, margin_t
    x1, y1 = margin_l + grid_w, margin_t + grid_h
    for c in range(GRID_COLS + 1):
        x = x0 + c * grid_w / GRID_COLS
        d.line((x, y0, x, y1), fill=(0,0,0,180), width=1)
    for r in range(GRID_ROWS + 1):
        y = y0 + r * grid_h / GRID_ROWS
        d.line((x0, y, x1, y), fill=(0,0,0,180), width=1)
    d.rectangle((x0, y0, x1, y1), outline=(0,0,0,255), width=2)

    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        cx = x0 + (col + 0.5) * grid_w / GRID_COLS
        cy = y0 + (row + 0.5) * grid_h / GRID_ROWS
        d.ellipse((cx-16, cy-16, cx+16, cy+16), outline=(0,0,0,255), width=3)
        d.text((cx+22, cy-10), f"TARGET\\n{target}", fill=(0,0,0,255))
        # yaw arrow
        import math as _math
        a = yaw * _math.pi / 180.0
        ex, ey = cx + 45*_math.cos(a), cy - 45*_math.sin(a)
        d.line((cx, cy, ex, ey), fill=(0,0,0,255), width=2)
        d.ellipse((ex-3, ey-3, ex+3, ey+3), fill=(0,0,0,255))

    # note
    d.rectangle((735, 110, 875, 250), outline=(0,0,0,255), width=2)
    d.multiline_text((750, 130), "Target object\\nspawns by grid cell\\n\\nYaw is randomized\\n\\nOther current asset\\nacts as distractor", fill=(0,0,0,255), spacing=5)

    img.save(out_path)


def colorize_semantic(seg):
    seg = np.asarray(seg, dtype=np.uint16)
    out = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8)
    palette = {
        0:  (0, 0, 0),
        2:  (255, 140, 0),    # scalpel_type2
        18: (0, 200, 0),      # tray
        21: (0, 120, 255),    # scalpel
        46: (180, 180, 180),  # robot
    }
    for k, color in palette.items():
        out[seg == k] = color
    return out


def export_segment_preview(recorder, out_dir, ep_idx, indices, meta):
    base_dir = os.path.join(out_dir, f"episode_{ep_idx:06d}_preview")
    os.makedirs(base_dir, exist_ok=True)
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    for sub in ["front_rgb", "front_depth", "front_semantic", "grip_b_rgb", "grip_b_depth", "grip_b_semantic", "front_mask"]:
        os.makedirs(os.path.join(base_dir, sub), exist_ok=True)

    selected = []
    if len(indices) > 0:
        selected = [indices[0], indices[-1]]
        # add stage transitions inside segment
        last = None
        for idx in indices:
            st = recorder.stage_names[idx]
            if st != last:
                selected.append(idx)
                last = st
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        for idx in indices[::max(1, CAMERA_EXPORT_STRIDE)]:
            selected.append(idx)
    selected = sorted(set(selected))

    for idx in selected:
        stage = _safe_name(recorder.stage_names[idx])
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        Image.fromarray(recorder.front_rgb[idx]).save(os.path.join(base_dir, "front_rgb", f"step_{idx:04d}_{stage}.png"))
        Image.fromarray(_depth_to_vis_uint8(recorder.front_depth[idx])).save(os.path.join(base_dir, "front_depth", f"step_{idx:04d}_{stage}.png"))
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        Image.fromarray(recorder.grip_b_rgb[idx]).save(os.path.join(base_dir, "grip_b_rgb", f"step_{idx:04d}_{stage}.png"))
        Image.fromarray(_depth_to_vis_uint8(recorder.grip_b_depth[idx])).save(os.path.join(base_dir, "grip_b_depth", f"step_{idx:04d}_{stage}.png"))

        front_sem = recorder.front_semantic[idx] if hasattr(recorder, "front_semantic") and idx < len(recorder.front_semantic) else np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH), dtype=np.uint16)
        grip_sem = recorder.grip_b_semantic[idx] if hasattr(recorder, "grip_b_semantic") and idx < len(recorder.grip_b_semantic) else np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH), dtype=np.uint16)
        mask_placeholder = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH), dtype=np.uint8)
        Image.fromarray(colorize_semantic(front_sem)).save(os.path.join(base_dir, "front_semantic", f"step_{idx:04d}_{stage}.png"))
        Image.fromarray(colorize_semantic(grip_sem)).save(os.path.join(base_dir, "grip_b_semantic", f"step_{idx:04d}_{stage}.png"))
        Image.fromarray(mask_placeholder).save(os.path.join(base_dir, "front_mask", f"step_{idx:04d}_{stage}.png"))

    draw_grid_preview_png(os.path.join(base_dir, "grid_preview.png"), meta)

    with open(os.path.join(base_dir, "preview_info.txt"), "w", encoding="utf-8") as f:
        f.write(json.dumps(meta, indent=2))
        f.write("\\n\\nselected frames:\\n")
        for idx in selected:
            f.write(f"{idx:04d} {recorder.stage_names[idx]}\\n")


def canonical_object_name(name):
    s = str(name).lower()
    aliases = {
        "love": "love_retractor",
        "love_retractor": "love_retractor",
        "retractor": "love_retractor",
        "scalpel_type2": "scalpel_type2",
        "scalpel_type2s": "scalpel_type2",
        "scissor": "scissor",
        "scissors": "scissor",
        "scalpel": "scalpel",
        "knife": "scalpel",
    }
    return aliases.get(s, s)


def stage_prefix_for_object(name):
    s = canonical_object_name(name)
    if s == "scalpel_type2":
        return "SCALPEL_TYPE2"
    if s == "love_retractor":
        return "LOVE"
    if s == "scissor":
        return "SCISSOR"
    if s == "scalpel":
        return "SCALPEL"
    return s.upper()


def stage_suffix_from_name(stage_name):
    st = str(stage_name)
    for pfx in ("SCALPEL_TYPE2_", "LOVE_RETRACTOR_", "SCISSOR_", "SCALPEL_", "LOVE_"):
        if st.startswith(pfx):
            return st[len(pfx):]
    return st.split("_", 1)[1] if "_" in st else st


def stage_id_from_name(stage_name):
    return int(STAGE_TYPE_IDS.get(stage_suffix_from_name(stage_name), -1))


def save_realcompat_segment(recorder, ep_idx, segment, out_dir, success, object_name, meta=None):
    if not success or not recorder.actions:
        return False

    object_name_l = canonical_object_name(object_name)
    stage_prefix = stage_prefix_for_object(object_name_l)
    suffixes = PICK_STAGE_SUFFIXES if segment == "pick" else PLACE_STAGE_SUFFIXES

    indices = []
    for i, st in enumerate(recorder.stage_names):
        if not st.startswith(stage_prefix + "_"):
            continue
        suffix = stage_suffix_from_name(st)
        if suffix in suffixes:
            indices.append(i)

    if not indices:
        print(f"[SEGMENT SAVE] no {segment} indices for {object_name}")
        return False

    os.makedirs(out_dir, exist_ok=True)

    states_legacy = np.asarray([recorder.states[i] for i in indices], dtype=np.float32)
    actions = np.asarray([recorder.actions[i] for i in indices], dtype=np.float32)
    stage_names = [recorder.stage_names[i] for i in indices]
    step_ids = np.asarray([recorder.step_ids[i] for i in indices], dtype=np.int32)

    obj_id = OBJECT_TYPE_IDS[object_name_l]
    skill_id = SKILL_TYPE_IDS[segment]
    states_realcompat = make_realcompat_state_from_legacy(states_legacy, obj_id, skill_id)
    robot_proprio = states_legacy[:, 0:16]
    target_slot = states_legacy[:, 30:33]
    object_type_id = np.full((len(indices), 1), obj_id, dtype=np.float32)
    skill_id_arr = np.full((len(indices), 1), skill_id, dtype=np.float32)
    stage_id_arr = np.asarray([stage_id_from_name(recorder.stage_names[i]) for i in indices], dtype=np.int32).reshape(-1, 1)
    stage_suffixes = [stage_suffix_from_name(recorder.stage_names[i]) for i in indices]

    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    front_rgb = np.asarray([recorder.front_rgb[i] for i in indices], dtype=np.uint8)
    front_depth = np.asarray([recorder.front_depth[i] for i in indices], dtype=np.float16)
    front_semantic = np.asarray([recorder.front_semantic[i] for i in indices], dtype=np.uint16)
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    grip_b_rgb = np.asarray([recorder.grip_b_rgb[i] for i in indices], dtype=np.uint8)
    grip_b_depth = np.asarray([recorder.grip_b_depth[i] for i in indices], dtype=np.float16)
    grip_b_semantic = np.asarray([recorder.grip_b_semantic[i] for i in indices], dtype=np.uint16)
    extra_camera_arrays = {}
    for _cam_name in PHASE3_EXTRA_CAMERA_NAMES:
        try:
            extra_camera_arrays[_cam_name] = (
                np.asarray([recorder.extra_camera_rgb[_cam_name][i] for i in indices], dtype=np.uint8),
                np.asarray([recorder.extra_camera_depth[_cam_name][i] for i in indices], dtype=np.float16),
                np.asarray([recorder.extra_camera_semantic[_cam_name][i] for i in indices], dtype=np.uint16),
            )
        except Exception as _e:
            print(f"[EXTRA CAMERA SAVE WARN] {_cam_name}: {_e!r}")


    T = len(indices)
    dones = np.zeros((T,), dtype=np.bool_)
    dones[-1] = True

    path = os.path.join(out_dir, f"episode_{ep_idx:06d}.h5")
    with h5py.File(path, "w") as f:
        f.attrs["semantic_mapping_version"] = "phase3_canonical_v1"
        f.attrs["semantic_class_ids"] = json.dumps({
            "background": 0,
            "robot": 1,
            "surgical_tray": 2,
            "scalpel": 3,
            "scissor": 4,
            "love_retractor": 5,
            "kelly": 6,
            "scalpel_type2": 7,
        })

        f.attrs["dataset_schema"] = "phase3_vision_pickplace_no_slot_v2"
        f.attrs["policy_skill"] = segment
        f.attrs["target_object"] = object_name_l
        f.attrs["object_type_id"] = int(PHASE3_TARGET_OBJECT_TYPE_ID)
        f.attrs["skill_id"] = int(skill_id)
        f.attrs["success"] = bool(success)
        f.attrs["num_samples"] = int(T)
        f.attrs["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.attrs["state_dim"] = int(REALCOMPAT_STATE_DIM)
        f.attrs["action_dim"] = ACTION_DIM
        f.attrs["state_keys"] = json.dumps(REALCOMPAT_STATE_KEYS)
        f.attrs["action_keys"] = json.dumps(ACTION_KEYS)
        f.attrs["object_type_ids"] = json.dumps(OBJECT_TYPE_IDS)
        f.attrs["skill_type_ids"] = json.dumps(SKILL_TYPE_IDS)
        f.attrs["stage_type_ids"] = json.dumps(STAGE_TYPE_IDS)
        f.attrs["stage_id_note"] = "stage_id is debug/analysis metadata; default policy input uses object_type_id and skill_id."
        f.attrs["distractor_policy_note"] = "target=scalpel_type2; current configured distractor: scalpel; scissor requires adding third RigidObjectCfg"
        f.attrs["state_frame"] = "robot_base"
        f.attrs["action_frame"] = "robot_base"
        f.attrs["action_type"] = "absolute_pose_quat_gripper_8d_baseframe"
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        f.attrs["camera_views"] = json.dumps(list(PHASE3_ALL_CAMERA_VIEWS))
        f.attrs["important"] = "Policy-safe observations exclude simulator ground-truth object poses. GT is stored only under debug_gt."
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        f.attrs["segmentation_note"] = "observations/*_semantic uses stable Phase3 canonical IDs: 0=background,1=robot,2=surgical_tray,3=scalpel,4=scissor,5=love_retractor,6=kelly,7=scalpel_type2. Do not interpret Isaac raw RGBA palette values as class IDs."

        if meta:
            for k, v in meta.items():
                try:
                    f.attrs[k] = v
                except Exception:
                    f.attrs[k] = str(v)

        obs = f.create_group("observations")
        obs.create_dataset("state", data=states_realcompat)
        obs.create_dataset("robot_proprio", data=robot_proprio)
        obs.create_dataset("object_type_id", data=object_type_id)
        obs.create_dataset("skill_id", data=skill_id_arr)
        obs.create_dataset("stage_id", data=stage_id_arr)

        obs.create_dataset("front_rgb", data=front_rgb, compression="gzip")
        obs.create_dataset("front_depth", data=front_depth, compression="gzip")
        obs.create_dataset("front_semantic", data=front_semantic, compression="gzip")
        obs.create_dataset("wrist_rgb", data=grip_b_rgb, compression="gzip")
        obs.create_dataset("wrist_depth", data=grip_b_depth, compression="gzip")

        # compatibility aliases
        obs.create_dataset("images_front", data=front_rgb, compression="gzip")
        obs.create_dataset("depth_front", data=front_depth, compression="gzip")
        obs.create_dataset("images_wrist", data=grip_b_rgb, compression="gzip")
        obs.create_dataset("depth_wrist", data=grip_b_depth, compression="gzip")
        obs.create_dataset("images_grip_b", data=grip_b_rgb, compression="gzip")
        obs.create_dataset("depth_grip_b", data=grip_b_depth, compression="gzip")
        obs.create_dataset("grip_b_semantic", data=grip_b_semantic, compression="gzip")
        # [PHASE3 EXTRA CAMERA H5 DATASETS]
        for _cam_name, (_rgb, _depth, _sem) in extra_camera_arrays.items():
            obs.create_dataset(f"{_cam_name}_rgb", data=_rgb, compression="gzip")
            obs.create_dataset(f"{_cam_name}_depth", data=_depth, compression="gzip")
            obs.create_dataset(f"{_cam_name}_semantic", data=_sem, compression="gzip")
        # selected_object_mask intentionally omitted: no verified target mask available.
        obs.create_dataset("segmentation_map", data=front_semantic, compression="gzip")

        f.create_dataset("actions", data=actions)
        f.create_dataset("dones", data=dones)
        f.create_dataset("rewards", data=np.zeros((T,), dtype=np.float32))
        f.create_dataset("stage_names", data=np.asarray(stage_names, dtype=h5py.string_dtype()))
        f.create_dataset("stage_suffixes", data=np.asarray(stage_suffixes, dtype=h5py.string_dtype()))
        f.create_dataset("step_ids", data=step_ids)

        dbg = f.create_group("debug_gt")
        dbg.create_dataset("target_slot_b", data=target_slot)
        dbg.create_dataset("legacy_state_34d", data=states_legacy)
        dbg.create_dataset("scalpel_type2_pose_b", data=states_legacy[:, 16:23])
        dbg.create_dataset("scalpel_pose_b", data=states_legacy[:, 23:30])
        if object_name_l == "scalpel_type2":
            dbg.create_dataset("selected_object_pose_b", data=states_legacy[:, 16:23])
        else:
            dbg.create_dataset("selected_object_pose_b", data=states_legacy[:, 23:30])

        ns = f.create_group("norm_stats")
        ns.create_dataset("state_mean", data=states_realcompat.mean(0).astype(np.float32))
        ns.create_dataset("state_std", data=(states_realcompat.std(0) + 1e-8).astype(np.float32))
        ns.create_dataset("action_mean", data=actions.mean(0).astype(np.float32))
        ns.create_dataset("action_std", data=(actions.std(0) + 1e-8).astype(np.float32))

    export_segment_preview(recorder, out_dir, ep_idx, indices, dict(meta or {}, policy_skill=segment, target_object=object_name_l))
    print(f"[SEGMENT SAVE] {segment} | object={object_name_l} | steps={T} | path={path}")
    return True

def compute_and_save_realcompat_norm_stats(out_dir):
    files=sorted(glob.glob(os.path.join(out_dir,"episode_*.h5")))
    if not files:
        print(f"[NORM STATS] no files in {out_dir}")
        return
    S,A=[],[]
    for fp in files:
        with h5py.File(fp,"r") as f:

            S.append(f["observations/state"][:])
            A.append(f["actions"][:])
    s=np.concatenate(S,0); a=np.concatenate(A,0)
    stats={
        "state":{"mean":s.mean(0).tolist(),"std":(s.std(0)+1e-8).tolist(),
                 "min":s.min(0).tolist(),"max":s.max(0).tolist()},
        "action":{"mean":a.mean(0).tolist(),"std":(a.std(0)+1e-8).tolist(),
                  "min":a.min(0).tolist(),"max":a.max(0).tolist()},
        "state_keys":REALCOMPAT_STATE_KEYS,
        "action_keys":ACTION_KEYS,
        "state_dim":REALCOMPAT_STATE_DIM,
        "action_dim":ACTION_DIM,
        "num_episodes":len(files),
        "total_steps":int(s.shape[0]),
        "dataset_schema":"phase3_realcompatible_split_skill_v1",
    }
    p=os.path.join(out_dir,"norm_stats.json")
    with open(p,"w") as f: json.dump(stats,f,indent=2)
    print(f"[NORM STATS] Saved -> {p}")


def sample_episode_spawn(rng):
    """
    Guaranteed 5-object spawn:
      scalpel, scissor, love_retractor, kelly, scalpel_type2

    Target object is PHASE3_TARGET_OBJECT.
    Distractors are exactly all other four objects.
    No duplicate scalpel. No missing scalpel_type2.
    """
    import math

    def sample_xy_for(name):
        # target/scissor grid/ranges remain handled by old constants where possible.
        if name == "scalpel":
            return {
                "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
                "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }

        if name == "scissor":
            return {
                "x": float(rng.uniform(*SCISSOR_RANDOM_X_RANGE)),
                "y": float(rng.uniform(*SCISSOR_RANDOM_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }

        # extras use shared table workspace. Keep away from extreme edges.
        return {
            "x": float(rng.uniform(0.34, 0.66)),
            "y": float(rng.uniform(0.04, 0.32)),
            "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
        }

    def xy_of(name, data):
        if name == "scalpel":
            return float(data["center_x"]), float(data["center_y"])
        return float(data["x"]), float(data["y"])

    last = None
    for _try in range(SPAWN_MAX_TRIES):
        params = {}

        for name in PHASE3_ALL_OBJECTS:
            params[name] = sample_xy_for(name)

        # keep old metadata style: grid exists, target info exists
        tx, ty = xy_of(PHASE3_TARGET_OBJECT, params[PHASE3_TARGET_OBJECT])
        params["grid"] = {
            "cell_id": int(_try),
            "row": -1,
            "col": -1,
            "x": float(tx),
            "y": float(ty),
            "target_object": PHASE3_TARGET_OBJECT,
            "target_yaw_deg": float(params[PHASE3_TARGET_OBJECT]["yaw_deg"]),
            "requested_num_distractors": 4,
            "actual_num_distractors": 4,
            "distractor_objects": ",".join(phase3_expected_distractors()),
            "actual_objects": ",".join(PHASE3_ALL_OBJECTS),
        }

        last = params

        ok = True
        names = PHASE3_ALL_OBJECTS
        for i in range(len(names)):
            xi, yi = xy_of(names[i], params[names[i]])
            for j in range(i + 1, len(names)):
                xj, yj = xy_of(names[j], params[names[j]])
                d = math.hypot(xi - xj, yi - yj)
                if d < SPAWN_MIN_OBJ_OBJ:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            phase3_validate_spawn_set(params)
            return params

    print("[SPAWN WARN] could not satisfy full 5-object spacing; using last sample")
    phase3_validate_spawn_set(last)
    return last

def sample_tray_center(rng, device, scalpel_type2_pos_w, scalpel_center_w):
    return torch.tensor(TRAY_FIXED_POS, device=device, dtype=torch.float32)


def force_scalpel_pose(env, pose_mode, spawn_params):
    if not FORCE_OBJECTS_DIRECT_AFTER_RESET:
        return
    obj = env.scene["scalpel"]
    yaw_deg = float(spawn_params["yaw_deg"])
    yaw_rad = yaw_deg * math.pi / 180.0
    if pose_mode == "EDGE_SIDE":
        q = make_scalpel_edge_side_quat(yaw_rad, env.device)
        center_z = TABLE_Z + SCALPEL_EDGE_CENTER_Z
    else:
        q = make_scalpel_broad_flat_quat(yaw_rad, env.device)
        center_z = TABLE_Z + SCALPEL_BROAD_CENTER_Z

    desired_center = (
        float(spawn_params["center_x"]),
        float(spawn_params["center_y"]),
        float(center_z),
    )
    root_pos = root_pos_from_desired_scalpel_center(q, desired_center, env.device)

    root_pose = torch.zeros((env.num_envs, 7), device=env.device)
    root_pose[:, 0:3] = root_pos.reshape(1,3)
    root_pose[:, 3:7] = q.reshape(1,4)
    root_vel = torch.zeros((env.num_envs, 6), device=env.device)
    obj.write_root_pose_to_sim(root_pose)
    obj.write_root_velocity_to_sim(root_vel)
    obj.update(dt=env.physics_dt)
    print(f"[SPAWN SCALPEL] mode={pose_mode} center=({desired_center[0]:.4f},{desired_center[1]:.4f},{desired_center[2]:.4f}) yaw={yaw_deg:.1f} root={[round(float(v),4) for v in root_pos.tolist()]}")

def force_episode_objects(env, spawn_params, scalpel_pose_mode=None):
    """
    Spawn all five objects exactly once.
    Target object is not special here; it also appears once in spawn_params.
    """
    phase3_validate_spawn_set(spawn_params)

    if "scissor" in spawn_params:
        force_scissor_pose(env, spawn_params["scissor"])

    if "scalpel" in spawn_params:
        mode = scalpel_pose_mode or choose_scalpel_pose_mode(1)
        force_scalpel_pose(env, mode, spawn_params["scalpel"])

    if "love_retractor" in spawn_params:
        if "force_love_retractor_pose" in globals():
            force_love_retractor_pose(env, spawn_params["love_retractor"])
        elif "force_extra_love_retractor_pose" in globals():
            force_extra_love_retractor_pose(env, spawn_params["love_retractor"])
        else:
            print("[SPAWN WARN] no love_retractor force function found")

    if "kelly" in spawn_params:
        if "force_kelly_pose" in globals():
            force_kelly_pose(env, spawn_params["kelly"])
        elif "force_extra_kelly_pose" in globals():
            force_extra_kelly_pose(env, spawn_params["kelly"])
        else:
            print("[SPAWN WARN] no kelly force function found")

    if "scalpel_type2" in spawn_params:
        if "force_scalpel_type2_pose" in globals():
            force_scalpel_type2_pose(env, spawn_params["scalpel_type2"])
        elif "force_extra_scalpel_type2_pose" in globals():
            force_extra_scalpel_type2_pose(env, spawn_params["scalpel_type2"])
        else:
            print("[SPAWN WARN] no scalpel_type2 force function found")

def compute_scalpel_grasp_pose(env, obj_raw, obj_quat, pose_mode):
    center_w = local_point_to_world(obj_raw, obj_quat, SCALPEL_LOCAL_CENTER, env.device)

    world_x = local_axis_to_world(obj_quat, (1.0,0.0,0.0), env.device)
    world_y = local_axis_to_world(obj_quat, (0.0,1.0,0.0), env.device)
    world_z = local_axis_to_world(obj_quat, (0.0,0.0,1.0), env.device)

    x_z = abs(float(world_x[2]))
    y_z = abs(float(world_y[2]))
    z_z = abs(float(world_z[2]))
    center_near_table = abs(float(center_w[2]) - TABLE_Z) <= 0.030

    if pose_mode == "EDGE_SIDE":
        accepted = (x_z >= SCALPEL_EDGE_X_AXIS_MIN_Z) and center_near_table
        long_name = SCALPEL_EDGE_LONG_AXIS.upper()
        world_long = world_z if long_name == "Z" else world_y
        rule = "EDGE_SIDE_X_VERTICAL"
    else:
        accepted = (y_z >= SCALPEL_FLAT_Y_AXIS_MIN_Z) and center_near_table
        long_name = SCALPEL_FLAT_LONG_AXIS.upper()
        world_long = world_z if long_name == "Z" else world_x
        rule = "BROAD_FLAT_Y_VERTICAL"

    print(f"\n[SCALPEL] origin=({float(obj_raw[0]):.4f},{float(obj_raw[1]):.4f},{float(obj_raw[2]):.4f}) mode={pose_mode}")
    print(f"  center_w=({float(center_w[0]):.4f},{float(center_w[1]):.4f},{float(center_w[2]):.4f})")
    print(f"  axis_x=({float(world_x[0]):+.3f},{float(world_x[1]):+.3f},{float(world_x[2]):+.3f})")
    print(f"  axis_y=({float(world_y[0]):+.3f},{float(world_y[1]):+.3f},{float(world_y[2]):+.3f})")
    print(f"  axis_z=({float(world_z[0]):+.3f},{float(world_z[1]):+.3f},{float(world_z[2]):+.3f})")
    print(f"  rule={rule} x_z={x_z:.3f} y_z={y_z:.3f} z_z={z_z:.3f} center_near_table={center_near_table} accepted={accepted}")

    if not accepted:
        return None, None, center_w

    grasp_w = center_w.clone()
    z_target = TABLE_Z + SCALPEL_GRASP_Z_ABOVE_TABLE
    z_target = max(SCALPEL_GRASP_Z_MIN, min(SCALPEL_GRASP_Z_MAX, z_target))
    grasp_w[2] = z_target

    long_xy_norm = torch.linalg.norm(world_long[:2]).item()
    if long_xy_norm < 1e-4:
        print(f"  [REJECT] selected long axis {long_name} has tiny XY norm")
        return None, None, center_w

    long_yaw = torch.atan2(world_long[1], world_long[0])
    grasp_yaw = long_yaw + torch.tensor(SCALPEL_GRASP_YAW_OFFSET, device=env.device)
    print(f"  using_long_axis={long_name} long_yaw_deg={float(grasp_yaw)*57.2958:.1f}")
    print(f"  grasp_target=({float(grasp_w[0]):.4f},{float(grasp_w[1]):.4f},{float(grasp_w[2]):.4f})")
    return grasp_w, grasp_yaw, center_w


# =============================================================================
# pick_and_place_object
# SCALPEL_TYPE2 branch is kept as before.
# SCALPEL branch now uses the verified USD local frame logic.
# =============================================================================

def pick_and_place_object(
    env, recorder, stage,
    obj_name, phase_id,
    grasp_above_table,
    body_offset_x, body_offset_y, body_offset_z,
    get_pos_fn, get_quat_fn,
    tray_slot_target_w, base_grip_quat,
    scalpel_pose_mode=None,
):
    obj_raw   = get_pos_fn(env)
    obj_quat  = get_quat_fn(env)
    resting_z = float(obj_raw[2])

    if obj_name == "SCALPEL":
        pose_mode = (scalpel_pose_mode or "BROAD_FLAT").upper()
        obj, grasp_yaw, body_center_w = compute_scalpel_grasp_pose(env, obj_raw, obj_quat, pose_mode)
        if obj is None:
            print("[SCALPEL FAIL] pose/grasp computation rejected")
            return False, resting_z, resting_z, get_scalpel_center_w(env)

        yaw_q      = yaw_quat_wxyz(grasp_yaw, env.device)
        grasp_quat = quat_mul(yaw_q.reshape(1,4), base_grip_quat.reshape(1,4))[0]
        st2_yaw_offset_q = yaw_quat_wxyz(torch.tensor(float(SCALPEL_TYPE2_GRASP_YAW_OFFSET_DEG) * math.pi / 180.0, device=env.device), env.device)
        grasp_quat = quat_mul(st2_yaw_offset_q.reshape(1,4), grasp_quat.reshape(1,4))[0]
        print(f"[SCALPEL_TYPE2 GRASP QUAT OFFSET APPLIED] yaw_offset_deg={SCALPEL_TYPE2_GRASP_YAW_OFFSET_DEG}")
        show_marker(stage, f"/World/Markers/{obj_name}/body_center", body_center_w, "body_center")

        # Extra axis markers for debug only.
        wx = local_axis_to_world(obj_quat, (1.0,0.0,0.0), env.device)
        wz = local_axis_to_world(obj_quat, (0.0,0.0,1.0), env.device)
        show_marker(stage, f"/World/Markers/{obj_name}/x_plus", body_center_w + 0.09 * wx, "x_axis")
        show_marker(stage, f"/World/Markers/{obj_name}/x_minus", body_center_w - 0.09 * wx, "x_axis")
        show_marker(stage, f"/World/Markers/{obj_name}/z_plus", body_center_w + 0.09 * wz, "z_axis")
        show_marker(stage, f"/World/Markers/{obj_name}/z_minus", body_center_w - 0.09 * wz, "z_axis")
    else:
        # SCALPEL_TYPE2: same working yaw-only logic as old script.
        contact_z = max(GRASP_Z_MIN, resting_z + grasp_above_table)
        obj_yaw   = yaw_from_quat_wxyz(obj_quat)
        cos_y=torch.cos(obj_yaw).item(); sin_y=torch.sin(obj_yaw).item()
        world_dx = body_offset_x*cos_y - body_offset_y*sin_y
        world_dy = body_offset_x*sin_y + body_offset_y*cos_y
        obj = obj_raw.clone()
        obj[0] = obj_raw[0]+world_dx
        obj[1] = obj_raw[1]+world_dy
        obj[2] = contact_z + body_offset_z
        print(f"\n[SCALPEL_TYPE2] origin=({float(obj_raw[0]):.4f},{float(obj_raw[1]):.4f},{float(obj_raw[2]):.4f})")
        print(f"  grasp=({float(obj[0]):.4f},{float(obj[1]):.4f},{float(obj[2]):.4f})")

        obj_yaw    = yaw_from_quat_wxyz(obj_quat)
        yaw_q      = yaw_quat_wxyz(obj_yaw, env.device)
        grasp_quat = quat_mul(yaw_q.reshape(1,4), base_grip_quat.reshape(1,4))[0]
        st2_yaw_offset_q = yaw_quat_wxyz(torch.tensor(float(SCALPEL_TYPE2_GRASP_YAW_OFFSET_DEG) * math.pi / 180.0, device=env.device), env.device)
        grasp_quat = quat_mul(st2_yaw_offset_q.reshape(1,4), grasp_quat.reshape(1,4))[0]
        print(f"[SCALPEL_TYPE2 GRASP QUAT OFFSET APPLIED] yaw_offset_deg={SCALPEL_TYPE2_GRASP_YAW_OFFSET_DEG}")

    # Waypoints.
    hover       = obj + torch.tensor([0.0,0.0, 0.23], device=env.device)
    pre         = obj + torch.tensor([0.0,0.0, 0.060],device=env.device)
    grasp       = obj.clone()

    close_grasp = grasp.clone()
    if obj_name == "SCALPEL":
        close_grasp[2] = max(SCALPEL_GRASP_Z_MIN, float(grasp[2]) - SCALPEL_LOWER_EXTRA_Z)

    micro_lift  = close_grasp + torch.tensor([0.0,0.0, 0.055],device=env.device)
    lift_mid    = close_grasp + torch.tensor([0.0,0.0, 0.16], device=env.device)
    lift        = close_grasp + torch.tensor([0.0,0.0, 0.28], device=env.device)
    place_above = tray_slot_target_w + torch.tensor([0.0,0.0, 0.18], device=env.device)
    lower       = tray_slot_target_w + torch.tensor([0.0,0.0, 0.035],device=env.device)
    retreat     = tray_slot_target_w + torch.tensor([0.0,0.0, 0.22], device=env.device)

    place_waypoint_markers(stage, obj_name, {
        "obj_origin":obj_raw,"obj_grasp_xy":obj,
        "hover":hover,"pre":pre,"grasp":grasp,"lower":close_grasp,
        "micro_lift":micro_lift,"lift_mid":lift_mid,"lift":lift,
        "place_above":place_above,"lower":lower,"retreat":retreat,"slot":tray_slot_target_w,
    })

    pfx=obj_name+"_"; mz=resting_z

    mz=max(mz,step_dynamic(env,recorder,pfx+"OPEN_HOVER",  hover,      grasp_quat,1.0, tray_slot_target_w,phase_id,max_steps=80, dist_thresh=0.025,settle_steps=4))
    mz=max(mz,step_dynamic(env,recorder,pfx+"LOWER_PRE",   pre,        grasp_quat,1.0, tray_slot_target_w,phase_id,max_steps=80, dist_thresh=0.020,settle_steps=4))

    _force = (obj_name == "SCALPEL")
    mz=max(mz,step_dynamic(env,recorder,pfx+"LOWER_GRASP", grasp,      grasp_quat,1.0, tray_slot_target_w,phase_id,max_steps=120,dist_thresh=0.008,settle_steps=8,force_wait=_force))

    if obj_name == "SCALPEL":
        mz=max(mz,step_dynamic(env,recorder,pfx+"LOWER_EXTRA", close_grasp, grasp_quat,1.0, tray_slot_target_w,phase_id,max_steps=50,dist_thresh=0.006,settle_steps=8,force_wait=True))

    hold_steps=20 if obj_name=="SCALPEL_TYPE2" else 30
    mz=max(mz,step_smooth_grip(env,recorder,pfx+"HOLD_BEFORE_CLOSE",close_grasp,grasp_quat,
                                1.0,1.0,tray_slot_target_w,phase_id,steps=hold_steps))

    ee_c=get_ee_pos_w(env); ob_c=get_pos_fn(env)
    xy_err=torch.linalg.norm((ee_c-(get_scalpel_center_w(env) if obj_name=="SCALPEL" else ob_c))[:2]).item()
    print(f"[{obj_name} PRE-CLOSE] ee_z={float(ee_c[2]):.4f} obj_z={float(ob_c[2]):.4f} xy_err_to_center={xy_err:.4f}")

    if obj_name == "SCALPEL_TYPE2":
        # SCALPEL_TYPE2: close must be immediate and stationary.
        # Do not use step_smooth_grip here, because its first 25% stays open
        # and the scalpel_type2 can slip before the fingers fully clamp.
        mz=max(mz,step_hold_const_grip(env,recorder,pfx+"CLOSE",close_grasp,grasp_quat,
                                        -1.0,tray_slot_target_w,phase_id,steps=100))

        mz=max(mz,step_hold_const_grip(env,recorder,pfx+"HOLD_AFTER_CLOSE",close_grasp,grasp_quat,
                                        -1.0,tray_slot_target_w,phase_id,steps=70))

        obj_after_close=get_pos_fn(env); close_z=float(obj_after_close[2])

        scalpel_type2_micro_lift = close_grasp + torch.tensor([0.0,0.0,0.070], device=env.device)
        mz=max(mz,step_dynamic(env,recorder,pfx+"MICRO_LIFT",scalpel_type2_micro_lift,grasp_quat,-1.0,
                                tray_slot_target_w,phase_id,max_steps=95,dist_thresh=0.020,settle_steps=8,
                                force_wait=True))
    else:
        # SCALPEL: keep smooth close, because scalpel grasp already works.
        mz=max(mz,step_smooth_grip(env,recorder,pfx+"CLOSE",close_grasp,grasp_quat,
                                    1.0,-1.0,tray_slot_target_w,phase_id,steps=60))

        mz=max(mz,step_hold_const_grip(env,recorder,pfx+"HOLD_AFTER_CLOSE",close_grasp,grasp_quat,
                                        -1.0,tray_slot_target_w,phase_id,steps=20))

        obj_after_close=get_pos_fn(env); close_z=float(obj_after_close[2])

        mz=max(mz,step_dynamic(env,recorder,pfx+"MICRO_LIFT",micro_lift,grasp_quat,-1.0,
                                tray_slot_target_w,phase_id,max_steps=55,dist_thresh=0.020,settle_steps=8))

    obj_after_micro=get_pos_fn(env)
    lift_thresh=0.006 if obj_name=="SCALPEL_TYPE2" else 0.008
    micro_ok=float(obj_after_micro[2])>close_z+lift_thresh
    print(f"[{obj_name} MICRO] close_z={close_z:.4f} after_z={float(obj_after_micro[2]):.4f} ok={micro_ok}")

    if not micro_ok:
        print(f"[{obj_name}] MICRO FAIL")
        return False,mz,close_z,(get_scalpel_center_w(env) if obj_name=="SCALPEL" else get_pos_fn(env))

    mz=max(mz,step_dynamic(env,recorder,pfx+"LIFT_MID",   lift_mid,   grasp_quat,-1.0,tray_slot_target_w,phase_id,max_steps=70, dist_thresh=0.030,settle_steps=6))
    mz=max(mz,step_dynamic(env,recorder,pfx+"LIFT",       lift,       grasp_quat,-1.0,tray_slot_target_w,phase_id,max_steps=90, dist_thresh=0.035,settle_steps=6))
    mz=max(mz,step_dynamic(env,recorder,pfx+"MOVE_PLACE", place_above,grasp_quat,-1.0,tray_slot_target_w,phase_id,max_steps=120,dist_thresh=0.050,settle_steps=4))
    mz=max(mz,step_dynamic(env,recorder,pfx+"LOWER_PLACE",lower,      grasp_quat,-1.0,tray_slot_target_w,phase_id,max_steps=80, dist_thresh=0.025,settle_steps=4))
    mz=max(mz,step_smooth_grip(env,recorder,pfx+"OPEN",lower,grasp_quat,-1.0,1.0,tray_slot_target_w,phase_id,steps=35))
    mz=max(mz,step_dynamic(env,recorder,pfx+"RETREAT",    retreat,    grasp_quat,1.0, tray_slot_target_w,phase_id,max_steps=80, dist_thresh=0.030,settle_steps=4))

    final_pos = get_scalpel_center_w(env) if obj_name=="SCALPEL" else get_pos_fn(env)
    return True,mz,close_z,final_pos


# =============================================================================
# Quality gate (identical to ok_dual_1)
# =============================================================================

def quality_ok(recorder, pfx):
    sc=Counter(recorder.stage_names)
    checks={
        pfx+"LOWER_GRASP":(5,None),pfx+"LIFT_MID":(10,None),pfx+"LIFT":(10,None),
        pfx+"MOVE_PLACE":(12,None),pfx+"CLOSE":(20,None),pfx+"OPEN":(20,None),
        pfx+"MICRO_LIFT":(5,None),pfx+"HOLD_BEFORE_CLOSE":(5,None),
        pfx+"HOLD_AFTER_CLOSE":(5,None),
    }
    ok=True
    for stage,(lo,hi) in checks.items():
        count=sc.get(stage,0)
        if lo and count<lo: print(f"[QUALITY] {stage} {count}<{lo} FAIL"); ok=False
    return ok

def compute_and_save_global_norm_stats(out_dir):
    files=sorted(glob.glob(os.path.join(out_dir,"episode_*.h5")))
    if not files: return
    S,A=[],[]
    for fp in files:
        with h5py.File(fp,"r") as f:

            S.append(f["observations/state"][:]);A.append(f["actions"][:])
    s=np.concatenate(S,0);a=np.concatenate(A,0)
    stats={"state":{"mean":s.mean(0).tolist(),"std":(s.std(0)+1e-8).tolist(),
                    "min":s.min(0).tolist(),"max":s.max(0).tolist()},
           "action":{"mean":a.mean(0).tolist(),"std":(a.std(0)+1e-8).tolist(),
                     "min":a.min(0).tolist(),"max":a.max(0).tolist()},
           "state_keys":STATE_KEYS,"action_keys":ACTION_KEYS,
           "state_dim":STATE_DIM,"action_dim":ACTION_DIM,
           "num_episodes":len(files),"total_steps":int(s.shape[0]),
           "pick_order":"scalpel_type2_only"}
    p=os.path.join(out_dir,"norm_stats.json")
    with open(p,"w") as f: json.dump(stats,f,indent=2)
    print(f"[NORM STATS] Saved -> {p}")

def get_existing_demo_count(out_dir):
    os.makedirs(out_dir,exist_ok=True)
    return len(sorted(glob.glob(os.path.join(out_dir,"episode_*.h5"))))

def save_progress(out_dir, saved_count, attempt):
    p=os.path.join(out_dir,"progress.json"); tmp=p+".tmp"
    with open(tmp,"w") as f:
        json.dump({"saved_count":int(saved_count),"attempt":int(attempt),
                   "updated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")},f,indent=2)
    os.replace(tmp,p)
    print(f"[CHECKPOINT] saved_count={saved_count} attempt={attempt}")


def clear_all_visualizer_prims(stage):
    """
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    Remove all USD visualizer/marker/grid prims so camera RGB cannot record them.
    DebugDraw overlays are also cleared.
    """
    bad_tokens = [
        "Phase3SpawnGrid",
        "Phase3GridDirectionCalibration",
        "GridDirectionCalibration",
        "GridDirection",
        "SpawnGrid",
        "WaypointMarker",
        "TargetMarker",
        "VisualMarker",
        "Marker",
        "Markers",
        "target_square",
        "red_square",
        "debug_grid",
    ]

    try:
        paths = []
        for prim in stage.Traverse():
            s = str(prim.GetPath())
            sl = s.lower()
            if any(tok.lower() in sl for tok in bad_tokens):
                paths.append(s)

        for s in sorted(set(paths), key=len, reverse=True):
            try:
                prim = stage.GetPrimAtPath(s)
                if prim.IsValid():
                    pass  # disabled: never RemovePrim during live PhysX simulation
                    print("[VIS CLEAN REMOVE]", s)
            except Exception:
                pass
    except Exception as e:
        print("[VIS CLEAN WARN]", repr(e))

    try:
        from omni.isaac.debug_draw import _debug_draw
        draw = _debug_draw.acquire_debug_draw_interface()
        try:
            draw.clear_points()
        except Exception:
            pass
        try:
            draw.clear_lines()
        except Exception:
            pass
    except Exception:
        pass


def draw_spawn_grid_usd(*args, **kwargs):
    return None


# =============================================================================
# PHASE3 FINAL OVERRIDE: 5 objects + stable training IDs
# =============================================================================

PHASE3_ALL_OBJECTS = ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"]
PHASE3_OBJECT_TYPE_ID = {
    "scalpel": 0,
    "scissor": 1,
    "love_retractor": 2,
    "kelly": 3,
    "scalpel_type2": 4,
}
PHASE3_TARGET_OBJECT = "scalpel_type2"
PHASE3_TARGET_OBJECT_TYPE_ID = 4

def phase3_expected_distractors():
    return [x for x in ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"] if x != PHASE3_TARGET_OBJECT]

def phase3_validate_spawn_set(spawn_params):
    all_objects = ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"]
    expected = set(all_objects)
    actual = set([k for k in all_objects if k in spawn_params])

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    print("[SPAWN SET CHECK] target=", PHASE3_TARGET_OBJECT)
    print("[SPAWN SET CHECK] expected=", all_objects)
    print("[SPAWN SET CHECK] actual=", sorted(actual))
    print("[SPAWN SET CHECK] missing=", missing, "duplicate=[]", "extra=", extra)

    if missing or extra:
        raise RuntimeError(f"BAD SPAWN SET: missing={missing} duplicate=[] extra={extra}")

    return True

def _phase3_xy_of(name, data):
    if name == "scalpel":
        return float(data["center_x"]), float(data["center_y"])
    return float(data["x"]), float(data["y"])

def _phase3_sample_one_object(rng, name):
    if name == "scalpel":
        return {
            "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
            "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
            "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
        }

    if name == "scissor":
        return {
            "x": float(rng.uniform(*SCISSOR_RANDOM_X_RANGE)),
            "y": float(rng.uniform(*SCISSOR_RANDOM_Y_RANGE)),
            "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
        }

    return {
        "x": float(rng.uniform(0.34, 0.66)),
        "y": float(rng.uniform(0.04, 0.32)),
        "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
    }

def sample_episode_spawn(rng):
    import math

    all_objects = ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"]
    last = None

    for attempt_i in range(SPAWN_MAX_TRIES):
        params = {}
        for name in all_objects:
            params[name] = _phase3_sample_one_object(rng, name)

        tx, ty = _phase3_xy_of(PHASE3_TARGET_OBJECT, params[PHASE3_TARGET_OBJECT])

        params["grid"] = {
            "cell_id": int(attempt_i),
            "row": -1,
            "col": -1,
            "x": float(tx),
            "y": float(ty),
            "target_object": PHASE3_TARGET_OBJECT,
            "target_yaw_deg": float(params[PHASE3_TARGET_OBJECT]["yaw_deg"]),
            "requested_num_distractors": 4,
            "actual_num_distractors": 4,
            "distractor_objects": ",".join([x for x in all_objects if x != PHASE3_TARGET_OBJECT]),
            "actual_objects": ",".join(all_objects),
            "object_type_id_map": "scalpel=0,scissor=1,love_retractor=2,kelly=3,scalpel_type2=4",
            "target_object_type_id": int(PHASE3_TARGET_OBJECT_TYPE_ID),
        }

        last = params

        ok = True
        for i, a in enumerate(all_objects):
            ax, ay = _phase3_xy_of(a, params[a])
            for b in all_objects[i+1:]:
                bx, by = _phase3_xy_of(b, params[b])
                d = math.hypot(ax - bx, ay - by)
                if d < SPAWN_MIN_OBJ_OBJ:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            phase3_validate_spawn_set(params)
            return params

    print("[SPAWN WARN] could not satisfy 5-object spacing; using last sample")
    phase3_validate_spawn_set(last)
    return last

def force_episode_objects(env, spawn_params, scalpel_pose_mode=None):
    phase3_validate_spawn_set(spawn_params)

    if "scalpel" in spawn_params:
        mode = scalpel_pose_mode or choose_scalpel_pose_mode(1)
        force_scalpel_pose(env, mode, spawn_params["scalpel"])

    if "scissor" in spawn_params:
        if "force_scissor_pose" in globals():
            force_scissor_pose(env, spawn_params["scissor"])
        else:
            print("[SPAWN ERROR] force_scissor_pose missing")

    if "love_retractor" in spawn_params:
        if "force_love_retractor_pose" in globals():
            force_love_retractor_pose(env, spawn_params["love_retractor"])
        elif "force_extra_love_retractor_pose" in globals():
            force_extra_love_retractor_pose(env, spawn_params["love_retractor"])
        else:
            print("[SPAWN ERROR] love_retractor force function missing")

    if "kelly" in spawn_params:
        if "force_kelly_pose" in globals():
            force_kelly_pose(env, spawn_params["kelly"])
        elif "force_extra_kelly_pose" in globals():
            force_extra_kelly_pose(env, spawn_params["kelly"])
        else:
            print("[SPAWN ERROR] kelly force function missing")

    if "scalpel_type2" in spawn_params:
        if "force_scalpel_type2_pose" in globals():
            force_scalpel_type2_pose(env, spawn_params["scalpel_type2"])
        elif "force_extra_scalpel_type2_pose" in globals():
            force_extra_scalpel_type2_pose(env, spawn_params["scalpel_type2"])
        else:
            print("[SPAWN ERROR] scalpel_type2 force function missing")

def phase3_force_complete_5object_spawn(rng, spawn_params):
    """
    Runtime safety fix:
    even if an old sample_episode_spawn() is still called, force final spawn_params to contain:
      scalpel, scissor, love_retractor, kelly, scalpel_type2
    """
    import math

    all_objects = ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"]

    def xy_of(name, data):
        if name == "scalpel":
            return float(data["center_x"]), float(data["center_y"])
        return float(data["x"]), float(data["y"])

    def sample_one(name):
        if name == "scalpel":
            return {
                "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
                "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }
        if name == "scissor":
            return {
                "x": float(rng.uniform(*SCISSOR_RANDOM_X_RANGE)),
                "y": float(rng.uniform(*SCISSOR_RANDOM_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }
        return {
            "x": float(rng.uniform(0.34, 0.66)),
            "y": float(rng.uniform(0.04, 0.32)),
            "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
        }

    # Add missing objects, especially scalpel_type2.
    for name in all_objects:
        if name not in spawn_params:
            for _ in range(SPAWN_MAX_TRIES):
                cand = sample_one(name)
                cx, cy = xy_of(name, cand)

                ok = True
                for other in all_objects:
                    if other not in spawn_params:
                        continue
                    ox, oy = xy_of(other, spawn_params[other])
                    if math.hypot(cx - ox, cy - oy) < SPAWN_MIN_OBJ_OBJ:
                        ok = False
                        break

                if ok:
                    spawn_params[name] = cand
                    print(f"[SPAWN FIX] added missing {name}: {cand}")
                    break

            if name not in spawn_params:
                spawn_params[name] = sample_one(name)
                print(f"[SPAWN FIX WARN] forced missing {name} without spacing guarantee: {spawn_params[name]}")

    # Fix grid metadata.
    if "grid" not in spawn_params:
        spawn_params["grid"] = {}

    target = PHASE3_TARGET_OBJECT if "PHASE3_TARGET_OBJECT" in globals() else "unknown"
    if target in spawn_params:
        tx, ty = xy_of(target, spawn_params[target])
    else:
        tx, ty = 0.0, 0.0

    spawn_params["grid"]["x"] = float(tx)
    spawn_params["grid"]["y"] = float(ty)
    spawn_params["grid"]["target_object"] = target
    spawn_params["grid"]["target_yaw_deg"] = float(spawn_params[target]["yaw_deg"]) if target in spawn_params else 0.0
    spawn_params["grid"]["requested_num_distractors"] = 4
    spawn_params["grid"]["actual_num_distractors"] = 4
    spawn_params["grid"]["distractor_objects"] = ",".join([x for x in all_objects if x != target])
    spawn_params["grid"]["actual_objects"] = ",".join(all_objects)
    spawn_params["grid"]["object_type_id_map"] = "scalpel=0,scissor=1,love_retractor=2,kelly=3,scalpel_type2=4"

    actual = sorted([x for x in all_objects if x in spawn_params])
    missing = sorted(set(all_objects) - set(actual))

    print("[SPAWN FINAL FIX CHECK] expected=", all_objects)
    print("[SPAWN FINAL FIX CHECK] actual=", actual)
    print("[SPAWN FINAL FIX CHECK] missing=", missing)

    if missing:
        raise RuntimeError(f"SPAWN STILL MISSING OBJECTS AFTER FIX: {missing}")

    return spawn_params

# =============================================================================
# PHASE3 GRID SPAWN FINAL 5-OBJECT FIX
# =============================================================================

def phase3_ensure_all_5_objects_in_spawn(spawn_params, target_object, rng):
    import math

    all_objects = ["scalpel", "scissor", "love_retractor", "kelly", "scalpel_type2"]

    def xy_of(name, data):
        if name == "scalpel":
            return float(data["center_x"]), float(data["center_y"])
        return float(data["x"]), float(data["y"])

    def sample_one(name):
        if name == "scalpel":
            return {
                "center_x": float(rng.uniform(*SCALPEL_RANDOM_CENTER_X_RANGE)),
                "center_y": float(rng.uniform(*SCALPEL_RANDOM_CENTER_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }

        if name == "scissor":
            return {
                "x": float(rng.uniform(*SCISSOR_RANDOM_X_RANGE)),
                "y": float(rng.uniform(*SCISSOR_RANDOM_Y_RANGE)),
                "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE)),
            }

        if name == "love_retractor":
            xr = globals().get("LOVE_RANDOM_X_RANGE", GRID_X_RANGE)
            yr = globals().get("LOVE_RANDOM_Y_RANGE", GRID_Y_RANGE)
            return {"x": float(rng.uniform(*xr)), "y": float(rng.uniform(*yr)), "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE))}

        if name == "kelly":
            xr = globals().get("KELLY_RANDOM_X_RANGE", GRID_X_RANGE)
            yr = globals().get("KELLY_RANDOM_Y_RANGE", GRID_Y_RANGE)
            return {"x": float(rng.uniform(*xr)), "y": float(rng.uniform(*yr)), "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE))}

        if name == "scalpel_type2":
            xr = globals().get("SCALPEL_TYPE2_RANDOM_X_RANGE", GRID_X_RANGE)
            yr = globals().get("SCALPEL_TYPE2_RANDOM_Y_RANGE", GRID_Y_RANGE)
            return {"x": float(rng.uniform(*xr)), "y": float(rng.uniform(*yr)), "yaw_deg": float(rng.uniform(*RANDOM_YAW_DEG_RANGE))}

        raise RuntimeError(f"unknown object: {name}")

    for name in all_objects:
        if name in spawn_params:
            continue

        placed = False
        for _ in range(500):
            cand = sample_one(name)
            cx, cy = xy_of(name, cand)

            ok = True
            for other in all_objects:
                if other not in spawn_params:
                    continue
                ox, oy = xy_of(other, spawn_params[other])
                if math.hypot(cx - ox, cy - oy) < SPAWN_MIN_OBJ_OBJ:
                    ok = False
                    break

            if ok:
                spawn_params[name] = cand
                print(f"[GRID 5OBJ FIX] added missing {name}: {cand}")
                placed = True
                break

        if not placed:
            spawn_params[name] = sample_one(name)
            print(f"[GRID 5OBJ FIX WARN] forced missing {name}: {spawn_params[name]}")

    if "grid" not in spawn_params:
        spawn_params["grid"] = {}

    tx, ty = xy_of(target_object, spawn_params[target_object])
    spawn_params["grid"]["x"] = float(tx)
    spawn_params["grid"]["y"] = float(ty)
    spawn_params["grid"]["target_object"] = target_object
    spawn_params["grid"]["target_yaw_deg"] = float(spawn_params[target_object]["yaw_deg"])
    spawn_params["grid"]["requested_num_distractors"] = 4
    spawn_params["grid"]["actual_num_distractors"] = 4
    spawn_params["grid"]["distractor_objects"] = ",".join([x for x in all_objects if x != target_object])
    spawn_params["grid"]["actual_objects"] = ",".join(all_objects)
    spawn_params["grid"]["object_type_id_map"] = "scalpel=0,scissor=1,love_retractor=2,kelly=3,scalpel_type2=4"

    actual = sorted([x for x in all_objects if x in spawn_params])
    missing = sorted(set(all_objects) - set(actual))
    print("[GRID 5OBJ CHECK] actual=", actual)
    print("[GRID 5OBJ CHECK] missing=", missing)

    if missing:
        raise RuntimeError(f"GRID 5OBJ FIX FAILED missing={missing}")

    return spawn_params

# =============================================================================
# PHASE3 ALL OBJECT NATIVE FORCE FUNCTIONS - SAFE SCENE KEY CHECK
# =============================================================================

def phase3_scene_has(env, key):
    return key in list(env.scene.keys())

def phase3_write_rigid_root_pose(env, scene_key, xyz, quat_wxyz, label):
    if not phase3_scene_has(env, scene_key):
        raise RuntimeError(f"{scene_key} scene key missing. keys={list(env.scene.keys())}")

    obj = env.scene[scene_key]
    root_pose = torch.zeros((env.num_envs, 7), device=env.device)
    root_pose[:, 0:3] = torch.tensor(xyz, device=env.device, dtype=torch.float32).reshape(1, 3)
    root_pose[:, 3:7] = quat_wxyz.reshape(1, 4)

    root_vel = torch.zeros((env.num_envs, 6), device=env.device)
    obj.write_root_pose_to_sim(root_pose)
    obj.write_root_velocity_to_sim(root_vel)
    obj.update(dt=env.physics_dt)

    print(f"[SPAWN {label}] root=({xyz[0]:.4f},{xyz[1]:.4f},{xyz[2]:.4f})")

def force_love_retractor_pose(env, spawn_params):
    yaw_rad = float(spawn_params["yaw_deg"]) * math.pi / 180.0
    q = yaw_quat_wxyz(torch.tensor(yaw_rad, device=env.device), env.device)
    x = float(spawn_params["x"])
    y = float(spawn_params["y"])
    z = float(globals().get("LOVE_SPAWN_ROOT_Z", 0.0010))
    phase3_write_rigid_root_pose(env, "love_retractor", [x, y, z], q, "LOVE")
    print(f"[SPAWN LOVE] yaw={spawn_params['yaw_deg']:.1f}")

def force_kelly_pose(env, spawn_params):
    yaw_rad = float(spawn_params["yaw_deg"]) * math.pi / 180.0
    q = yaw_quat_wxyz(torch.tensor(yaw_rad, device=env.device), env.device)
    x = float(spawn_params["x"])
    y = float(spawn_params["y"])
    z = float(globals().get("KELLY_SPAWN_ROOT_Z", 0.0140))
    phase3_write_rigid_root_pose(env, "kelly", [x, y, z], q, "KELLY")
    print(f"[SPAWN KELLY] yaw={spawn_params['yaw_deg']:.1f}")

def force_scalpel_type2_pose(env, spawn_params):
    yaw_rad = float(spawn_params["yaw_deg"]) * math.pi / 180.0
    q = yaw_quat_wxyz(torch.tensor(yaw_rad, device=env.device), env.device)
    x = float(spawn_params["x"])
    y = float(spawn_params["y"])
    z = float(globals().get("SCALPEL_TYPE2_SPAWN_ROOT_Z", 0.0100))
    # ScalpelType2 is the canonical target read by its trajectory/state code.
    phase3_write_rigid_root_pose(env, "object", [x, y, z], q, "SCALPEL_TYPE2")
    print(f"[SPAWN SCALPEL_TYPE2] yaw={spawn_params['yaw_deg']:.1f}")

def force_extra_love_retractor_pose(env, spawn_params):
    return force_love_retractor_pose(env, spawn_params)

def force_extra_kelly_pose(env, spawn_params):
    return force_kelly_pose(env, spawn_params)

def force_extra_scalpel_type2_pose(env, spawn_params):
    return force_scalpel_type2_pose(env, spawn_params)

# =============================================================================
# PHASE3 SCISSOR DISTRACTOR FORCE FUNCTION
# =============================================================================

def force_scissor_pose(env, spawn_params):
    yaw_rad = float(spawn_params["yaw_deg"]) * math.pi / 180.0
    q = yaw_quat_wxyz(torch.tensor(yaw_rad, device=env.device), env.device)

    x = float(spawn_params["x"])
    y = float(spawn_params["y"])
    z = float(globals().get("SCISSOR_SPAWN_ROOT_Z", 0.0025))

    if "phase3_write_rigid_root_pose" in globals():
        phase3_write_rigid_root_pose(env, "scissor", [x, y, z], q, "SCISSOR")
    else:
        if "scissor" not in list(env.scene.keys()):
            raise RuntimeError(f"scissor scene key missing. keys={list(env.scene.keys())}")

        obj = env.scene["scissor"]
        root_pose = torch.zeros((env.num_envs, 7), device=env.device)
        root_pose[:, 0:3] = torch.tensor([x, y, z], device=env.device, dtype=torch.float32).reshape(1, 3)
        root_pose[:, 3:7] = q.reshape(1, 4)

        root_vel = torch.zeros((env.num_envs, 6), device=env.device)
        obj.write_root_pose_to_sim(root_pose)
        obj.write_root_velocity_to_sim(root_vel)
        obj.update(dt=env.physics_dt)

    print(f"[SPAWN SCISSOR] root=({x:.4f},{y:.4f},{z:.4f}) yaw={spawn_params['yaw_deg']:.1f}")

def force_extra_scissor_pose(env, spawn_params):
    return force_scissor_pose(env, spawn_params)

# =============================================================================
# PHASE3 ENSURE ALL 5 OBJECT SCENE CFG KEYS
# =============================================================================

def phase3_ensure_all_object_scene_cfg(env_cfg):
    """
    Ensure every recorder has explicit env.scene keys:
      scalpel, scissor, love_retractor, kelly, scalpel_type2

    Does not edit USD files.
    Does not overwrite keys that already exist.
    """
    from isaaclab.assets import RigidObjectCfg
    from isaaclab.sim import UsdFileCfg, RigidBodyPropertiesCfg, CollisionPropertiesCfg, MassPropertiesCfg

    def has_scene_attr(name):
        return hasattr(env_cfg.scene, name)

    def add_obj(name, prim_name, usd_path, scale, pos, mass=0.12, lin_damp=0.8, ang_damp=4.0, contact=0.003):
        if has_scene_attr(name):
            return

        setattr(
            env_cfg.scene,
            name,
            RigidObjectCfg(
                prim_path="{ENV_REGEX_NS}/" + prim_name,
                spawn=UsdFileCfg(
                    usd_path=usd_path,
                    semantic_tags=[("class", name)],
                    scale=scale,
                    rigid_props=RigidBodyPropertiesCfg(
                        disable_gravity=False,
                        linear_damping=lin_damp,
                        angular_damping=ang_damp,
                    ),
                    collision_props=CollisionPropertiesCfg(
                        contact_offset=contact,
                        rest_offset=0.0,
                    ),
                    mass_props=MassPropertiesCfg(mass=mass),
                ),
                init_state=RigidObjectCfg.InitialStateCfg(
                    pos=pos,
                    rot=(1.0, 0.0, 0.0, 0.0),
                ),
            ),
        )
        print(f"[SCENE CFG ADD] {name} -> {prim_name}")

    add_obj(
        "scalpel",
        "Scalpel",
        SCALPEL_USD,
        (1.0, 1.0, 1.0),
        (0.52, 0.10, 0.0664),
        mass=0.03,
        lin_damp=0.8,
        ang_damp=4.0,
        contact=0.002,
    )

    add_obj(
        "scissor",
        "Scissor",
        SCISSOR_USD,
        (0.01, 0.01, 0.01),
        (0.42, 0.18, 0.0025),
        mass=0.08,
        lin_damp=0.8,
        ang_damp=4.0,
        contact=0.003,
    )

    add_obj(
        "love_retractor",
        "LoveRetractor",
        LOVE_USD_PATH,
        (0.00075, 0.00075, 0.00075),
        (0.48, 0.24, 0.0010),
        mass=0.12,
        lin_damp=0.8,
        ang_damp=4.0,
        contact=0.003,
    )

    add_obj(
        "kelly",
        "Kelly",
        KELLY_USD_PATH,
        (0.60, 0.60, 0.60),
        (0.56, 0.24, 0.0140),
        mass=0.12,
        lin_damp=0.8,
        ang_damp=4.0,
        contact=0.003,
    )

    add_obj(
        "scalpel_type2",
        "ScalpelType2",
        SCALPEL_TYPE2_USD_PATH,
        (0.00475421, 0.00475421, 0.00475421),
        (0.62, 0.28, 0.0100),
        mass=0.12,
        lin_damp=0.8,
        ang_damp=4.0,
        contact=0.003,
    )


def phase3_force_scalpel_type2_object_and_distractor_cfg(env_cfg):
    """Force target scene key object and distractor scene key scalpel_type2 to same USD/scale."""
    from isaaclab.assets import RigidObjectCfg
    from isaaclab.sim import UsdFileCfg, RigidBodyPropertiesCfg, MassPropertiesCfg, CollisionPropertiesCfg

    usd = SCALPEL_TYPE2_USD_PATH
    scale = SCALPEL_TYPE2_SCALE
    z = SCALPEL_TYPE2_SPAWN_ROOT_Z

    common_spawn = dict(
        usd_path=usd,
        scale=scale,
        rigid_props=RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        mass_props=MassPropertiesCfg(mass=0.03),
        collision_props=CollisionPropertiesCfg(),
    )

    env_cfg.scene.object = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Object",
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.37, 0.075, z),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
        spawn=UsdFileCfg(**common_spawn),
    )

    env_cfg.scene.scalpel_type2 = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/ScalpelType2",
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.61, 0.30, z),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
        spawn=UsdFileCfg(
                semantic_tags=[("class", "scalpel_type2")],**common_spawn),
    )

    print("[SCALPEL_TYPE2 FORCE CFG]")
    print("  object.usd        =", usd)
    print("  scalpel_type2.usd =", usd)
    print("  object.scale      =", scale)
    print("  scalpel_type2.scale=", scale)
    print("  spawn_z           =", z)
    return env_cfg


def phase3_stage_object_aliases(obj_name):
    """Return accepted stage prefixes for segment saving."""
    if obj_name == "scalpel_type2":
        return ("SCALPEL_TYPE2",)
    return (str(obj_name).upper(),)


def phase3_save_prefix_for_object(obj_name):
    return "SCALPEL_TYPE2" if obj_name == "scalpel_type2" else str(obj_name).upper()


# ============================================================
# PHASE3 RECORD MODE
# --record_mode both  : save pick + place
# --record_mode pick  : save pick only
# --record_mode place : save place only
# ============================================================

PHASE3_RECORD_MODE = "both"


def phase3_should_save_segment(segment_name):
    mode = phase3_get_record_mode()
    seg = str(segment_name).lower().strip()

    if mode in ["both", "all", "pickplace", "pick_place"]:
        return True
    if mode == "pick":
        return "pick" in seg
    if mode == "place":
        return "place" in seg
    return True

def phase3_detect_segment_from_locals(_loc):
    # Try common variable names first.
    for k in [
        "segment_name", "segment", "split", "split_name", "policy",
        "policy_name", "skill", "skill_name", "phase", "phase_name",
        "save_kind", "kind",
    ]:
        if k in _loc:
            v = str(_loc.get(k))
            vl = v.lower()
            if "pick" in vl or "place" in vl:
                return v

    # Fallback: scan local values.
    for v in _loc.values():
        try:
            s = str(v)
        except Exception:
            continue
        sl = s.lower()
        if "pick_policy" in sl or sl == "pick" or " pick" in sl:
            return "pick"
        if "place_policy" in sl or sl == "place" or " place" in sl:
            return "place"

    return "unknown"



def phase3_prune_outputs_by_record_mode(out_dir):
    from pathlib import Path
    import shutil

    mode = phase3_get_record_mode()
    root = Path(out_dir)

    if mode in ["both", "all", "pickplace", "pick_place"]:
        print(f"[RECORD_MODE PRUNE FINAL] keep both | mode={mode} | root={root}")
        return

    if mode == "pick":
        bad = root / "place_policy"
        if bad.exists():
            shutil.rmtree(bad, ignore_errors=True)
            print(f"[RECORD_MODE PRUNE FINAL] removed place_policy because record_mode=pick -> {bad}")
        else:
            print(f"[RECORD_MODE PRUNE FINAL] place_policy already absent | root={root}")
        return

    if mode == "place":
        bad = root / "pick_policy"
        if bad.exists():
            shutil.rmtree(bad, ignore_errors=True)
            print(f"[RECORD_MODE PRUNE FINAL] removed pick_policy because record_mode=place -> {bad}")
        else:
            print(f"[RECORD_MODE PRUNE FINAL] pick_policy already absent | root={root}")
        return

    print(f"[RECORD_MODE PRUNE FINAL] unknown mode={mode}, keep outputs | root={root}")



def phase3_force_viewer_debug_object_pose(env):
    import torch
    try:
        obj = env.scene["object"]
        root = obj.data.root_state_w.clone()
        root[:, 0] = 0.500000
        root[:, 1] = 0.000000
        root[:, 2] = 0.055000
        root[:, 3] = 1.000000
        root[:, 4] = 0.000000
        root[:, 5] = 0.000000
        root[:, 6] = 0.000000
        root[:, 7:] = 0.0
        obj.write_root_state_to_sim(root)
        env.sim.step()
        print("[PHASE3 DEBUG OBJECT POSE FORCED] object=(0.5,0.0,0.055) quat=(1,0,0,0)")
    except Exception as e:
        print("[PHASE3 DEBUG OBJECT POSE FORCE WARN]", repr(e))



# === PHASE3 GRIP CAMERA CONSTANT ALIASES FROM TUNER ===
try:
    from phase3_camera_tuning import PHASE3_CAMERAS as _PHASE3_CAMERAS_FOR_GRIP_ALIAS
    GRIP_B_POS = tuple(_PHASE3_CAMERAS_FOR_GRIP_ALIAS["grip_cam_b"]["pos"])
    GRIP_B_ROT = tuple(_PHASE3_CAMERAS_FOR_GRIP_ALIAS["grip_cam_b"]["rot"])
    GRIP_B_ROT90_K = GRIP_B_ROT
except Exception:
    GRIP_B_POS = (0.061365, 0.017054, 0.040467)
    GRIP_B_ROT = (-0.64681794, 0.15352391, 0.25956301, -0.70048840)
    GRIP_B_ROT90_K = GRIP_B_ROT
# === END PHASE3 GRIP CAMERA CONSTANT ALIASES FROM TUNER ===


def main():
    global ALL_PHASE3_OBJECTS, PHASE3_ALL_OBJECTS
    apply_workspace_globals(globals())
    ALL_PHASE3_OBJECTS = ENV_REQUEST.instruments
    PHASE3_ALL_OBJECTS = ENV_REQUEST.instruments
    print("[CONFIG] SCALPEL_TYPE2 ONLY | direct random spawn | same schema for shared multitask training")
    print(f"  SCALPEL_USD={SCALPEL_USD}")
    print(f"  SCALPEL_LOCAL_CENTER={SCALPEL_LOCAL_CENTER}")
    print(f"  SCALPEL_GRASP_Z_ABOVE_TABLE={SCALPEL_GRASP_Z_ABOVE_TABLE}  SCALPEL_LOWER_EXTRA_Z={SCALPEL_LOWER_EXTRA_Z}")
    print(f"  SCALPEL_POSE_SEQUENCE={SCALPEL_POSE_SEQUENCE}")
    print(f"  SPAWN_MIN_OBJ_OBJ={SPAWN_MIN_OBJ_OBJ}  SPAWN_MIN_OBJ_TRAY={SPAWN_MIN_OBJ_TRAY}")
    print(f"  SCISSOR_SCALE={SCISSOR_SCALE} SCISSOR_SPAWN_ROOT_Z={SCISSOR_SPAWN_ROOT_Z}")
    print(f"  LOVE_SCALE={LOVE_SCALE} LOVE_SPAWN_ROOT_Z={LOVE_SPAWN_ROOT_Z}")
    print(f"  SCALPEL_TYPE2_SCALE={SCALPEL_TYPE2_SCALE} SCALPEL_TYPE2_SPAWN_ROOT_Z={SCALPEL_TYPE2_SPAWN_ROOT_Z}")
    print(f"  GRIP_CAM_OUTSIDE pos={GRIP_B_POS} rot={GRIP_B_ROT} rot90={GRIP_B_ROT90_K}")
    print(f"  SCALPEL_TYPE2_USD_PATH={SCALPEL_TYPE2_USD_PATH}")
    print(f"  SCALPEL_TYPE2_SCALE={SCALPEL_TYPE2_SCALE}")
    phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
    print("[CAM STRICT PATCH] true RGB helper inserted; RGB must come from camera.data.output['rgb']")
    print(f"  VIS_GRID_FINE_TUNE spawn_x={GRID_X_RANGE} spawn_y={GRID_Y_RANGE} visual_x={VIS_GRID_X_RANGE} visual_y={VIS_GRID_Y_RANGE} tray={TRAY_FIXED_POS} yaw={TRAY_FIXED_YAW_DEG}")
    print("  SCALPEL_TYPE2_CLOSE=hard constant -1.0, then HOLD_AFTER_CLOSE before micro-lift")

    env_cfg=parse_env_cfg(args_cli.task,device=args_cli.device,num_envs=args_cli.num_envs)
    phase3_ensure_all_object_scene_cfg(env_cfg)

    try:
        if hasattr(env_cfg,"commands") and hasattr(env_cfg.commands,"object_pose"):
            env_cfg.commands.object_pose.debug_vis=False
            for attr in ("goal_pose_visualizer_cfg","current_pose_visualizer_cfg"):
                if hasattr(env_cfg.commands.object_pose,attr):
                    setattr(env_cfg.commands.object_pose,attr,None)
    except: pass

    from isaaclab.sim import (UsdFileCfg,RigidBodyPropertiesCfg,CollisionPropertiesCfg,MassPropertiesCfg)

    env_cfg.scene.object.spawn=UsdFileCfg(
        usd_path=SCALPEL_TYPE2_USD_PATH,scale=SCALPEL_TYPE2_SCALE,
        rigid_props=RigidBodyPropertiesCfg(disable_gravity=False),
        collision_props=CollisionPropertiesCfg(contact_offset=0.008,rest_offset=0.0002),
        mass_props=MassPropertiesCfg(mass=0.10),
    )
    if hasattr(env_cfg,"events") and hasattr(env_cfg.events,"reset_object_position"):
        env_cfg.events.reset_object_position.params["asset_cfg"].body_names=["Object"]
        if "pose_range" in env_cfg.events.reset_object_position.params:
            env_cfg.events.reset_object_position.params["pose_range"]["yaw"]=(-3.1416,3.1416)

    from isaaclab.assets import RigidObjectCfg
    from isaaclab.sim import UsdFileCfg as _UF
    env_cfg.scene.scalpel=RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Scalpel",
        spawn=_UF(
            semantic_tags=[("class", "scalpel")],usd_path=SCALPEL_USD,scale=(1.0,1.0,1.0),
                  rigid_props=RigidBodyPropertiesCfg(
                      disable_gravity=False,
                      linear_damping=0.8,
                      angular_damping=4.0,
                  ),
                  collision_props=CollisionPropertiesCfg(contact_offset=0.003,rest_offset=0.0),
                  mass_props=MassPropertiesCfg(mass=0.12)),
        # Overwritten every episode by force_scalpel_pose(); this is only a safe initial pose.
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.55,0.20,0.0664),rot=(1.0,0.0,0.0,0.0)),
    )


    # Extra distractor #2: scissor
    env_cfg.scene.scissor=RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Scissor",
        spawn=_UF(
            semantic_tags=[("class", "scissor")],usd_path=SCISSOR_USD,scale=SCISSOR_SCALE,
                  rigid_props=RigidBodyPropertiesCfg(
                      disable_gravity=False,
                      linear_damping=0.8,
                      angular_damping=4.0,
                  ),
                  collision_props=CollisionPropertiesCfg(contact_offset=0.003,rest_offset=0.0),
                  mass_props=MassPropertiesCfg(mass=0.12)),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.45,0.28,0.0025),rot=(1.0,0.0,0.0,0.0)),
    )


    # Extra distractor: love_retractor
    env_cfg.scene.love_retractor=RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/LoveRetractor",
        spawn=_UF(
            semantic_tags=[("class", "love_retractor")],usd_path=LOVE_USD_PATH,scale=LOVE_SCALE,
                  rigid_props=RigidBodyPropertiesCfg(
                      disable_gravity=False,
                      linear_damping=0.8,
                      angular_damping=4.0,
                  ),
                  collision_props=CollisionPropertiesCfg(contact_offset=0.003,rest_offset=0.0),
                  mass_props=MassPropertiesCfg(mass=0.10)),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.45,0.28,0.002),rot=(1.0,0.0,0.0,0.0)),
    )

    if hasattr(env_cfg,"terminations"):
        if hasattr(env_cfg.terminations,"time_out"):        env_cfg.terminations.time_out=None
        if hasattr(env_cfg.terminations,"object_dropping"): env_cfg.terminations.object_dropping=None

    # Front/global camera: scene overview.
        env_cfg.scene.camera=CameraCfg(
        prim_path="{ENV_REGEX_NS}/Camera",
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=16.0,
            horizontal_aperture=20.955,
            clipping_range=(0.01,10.0),
        ),
        width=CAMERA_WIDTH,height=CAMERA_HEIGHT,data_types=["rgb","distance_to_image_plane","semantic_segmentation"],update_period=0,
        offset=CameraCfg.OffsetCfg(
            pos=(0.88, 0.00, 0.50),
            rot=(0.27131, -0.64716, -0.65462, 0.28115),
        ),
    )

    # Final selected gripper camera: grip_b.
    # It is attached to panda_hand and then the saved image is rotated upright.

    env_cfg.scene.grip_cam_b=CameraCfg(
        prim_path=GRIP_B_CAMERA_PRIM,
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=14.0,
            horizontal_aperture=20.955,
            clipping_range=(0.001,2.0),
        ),
        width=CAMERA_WIDTH,height=CAMERA_HEIGHT,data_types=["rgb","distance_to_image_plane","semantic_segmentation"],update_period=0,
        offset=CameraCfg.OffsetCfg(
            pos=GRIP_B_POS,
            rot=GRIP_B_ROT,
        ),
    )
    # FINAL override: old copied code may overwrite env_cfg.scene.object before this.
    # Force target object and distractor scalpel_type2 to same USD/scale immediately before gym.make.
    env_cfg = phase3_force_scalpel_type2_object_and_distractor_cfg(env_cfg)


    # PHASE3 FINAL ROBOT SEMANTIC - before gym.make / PhysX init
    try:
        if hasattr(env_cfg.scene.robot, "spawn") and env_cfg.scene.robot.spawn is not None:
            env_cfg.scene.robot.spawn.semantic_tags = [("class", "robot")]
            print("[SEMANTIC CFG] robot -> robot")
        else:
            print("[SEMANTIC CFG WARN] env_cfg.scene.robot.spawn unavailable")
    except Exception as e:
        print("[SEMANTIC CFG WARN] robot semantic:", repr(e))

    apply_shared_env_cfg(
        env_cfg, ENV_REQUEST, camera_width=CAMERA_WIDTH, camera_height=CAMERA_HEIGHT,
        grip_camera_prim=GRIP_B_CAMERA_PRIM, grip_pos=GRIP_B_POS, grip_rot=GRIP_B_ROT)
    phase3_apply_final_cameras_to_env_cfg(env_cfg)

    env = gym.make(args_cli.task,cfg=env_cfg).unwrapped

    phase3_dump_runtime_alignment("scalpel_type2_recorder_after_gym_make")
    stage = omni.usd.get_context().get_stage()
    phase3_hide_all_debug_visuals(stage, verbose=True)
    recorder=EpisodeRecorder(args_cli.out_dir,args_cli.task_text,args_cli.debug_every)

    print("[ENV READY] scene keys:",list(env.scene.keys()),"device:",env.device)

    print("\n" + "="*120)
    print("[PHASE3 LIVE SEMANTIC INFO]")
    print("="*120)

    import json as _json
    import numpy as _np

    for _cam_name in [
        "camera",
        "grip_cam_b",
        "cam_top",
        "cam_left",
        "cam_right",
        "cam_tray",
    ]:
        try:
            _cam = env.scene[_cam_name]

            print("\n[CAM]", _cam_name)

            _sem = _cam.data.output.get("semantic_segmentation", None)
            if _sem is not None:
                _arr = _sem[0].detach().cpu().numpy()
                if _arr.ndim == 3:
                    _arr = _arr[..., 0]
                print("RAW_IDS =", _np.unique(_arr).tolist())
            else:
                print("RAW_IDS = <NO semantic tensor>")

            _info_all = getattr(_cam.data, "info", {})

            print("INFO_CONTAINER_TYPE =", type(_info_all))
            try:
                print("INFO_CONTAINER_LEN =", len(_info_all))
            except Exception:
                print("INFO_CONTAINER_LEN = NA")

            try:
                print("FULL_INFO_JSON =")
                print(_json.dumps(_info_all, indent=2, default=str))
            except Exception:
                print("FULL_INFO =", _info_all)

            _info = None

            if isinstance(_info_all, dict):
                _info = _info_all.get("semantic_segmentation", None)

            elif isinstance(_info_all, (list, tuple)):
                for _idx, _item in enumerate(_info_all):
                    print(f"\nINFO_ITEM[{_idx}] TYPE =", type(_item))

                    try:
                        print(_json.dumps(_item, indent=2, default=str))
                    except Exception:
                        print(_item)

                    if isinstance(_item, dict):
                        if "semantic_segmentation" in _item:
                            _info = _item["semantic_segmentation"]

                        for _k, _v in _item.items():
                            if "semantic" in str(_k).lower():
                                print("SEMANTIC_CANDIDATE =", _k)
                                try:
                                    print(_json.dumps(_v, indent=2, default=str))
                                except Exception:
                                    print(_v)

            print("EXTRACTED_SEM_INFO_TYPE =", type(_info))

            try:
                print("EXTRACTED_SEM_INFO_JSON =")
                print(_json.dumps(_info, indent=2, default=str))
            except Exception:
                print("EXTRACTED_SEM_INFO =", _info)

        except Exception as _e:
            print("[CAM ERROR]", _cam_name, repr(_e))

    print("\n" + "="*120)
    print("[END PHASE3 LIVE SEMANTIC INFO]")
    print("="*120)


    base_grip_quat=torch.tensor([0.0,0.7071,0.7071,0.0],device=env.device)
    target_success=args_cli.episodes
    saved_count=get_existing_demo_count(args_cli.out_dir) if args_cli.resume else 0
    attempt=0
    rng=np.random.default_rng(RANDOM_SEED)

    while saved_count < target_success:
        attempt+=1; recorder._reset()
        print(f"\n{'='*60}\n  ATTEMPT {attempt} | SUCCESS {saved_count}/{target_success}\n{'='*60}")

        env.reset()
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage(), verbose=True)


        hide_all_markers(stage)

        old=stage.GetPrimAtPath("/World/RandomTray")
        if old.IsValid(): stage.RemovePrim("/World/RandomTray")


        old_proxy = stage.GetPrimAtPath("/World/DEBUG_OBJECT_VISIBILITY_PROXY")
        if old_proxy.IsValid():
                    pass  # disabled: never RemovePrim during live PhysX simulation
        old_grid = stage.GetPrimAtPath("/World/Phase3SpawnGrid")
        if old_grid.IsValid():
                    pass  # disabled: never RemovePrim during live PhysX simulation
        # Remove cyan grip-camera debug visual if it exists.
        phase3_hide_all_debug_visuals(omni.usd.get_context().get_stage())
        # It can enter the real camera RGB image and corrupt training data.
        for _p in []:
            _old = stage.GetPrimAtPath(_p)
            if _old.IsValid():
                    pass  # disabled: never RemovePrim during live PhysX simulation
        scalpel_pose_mode=choose_scalpel_pose_mode(attempt)
        spawn_params=sample_episode_spawn_grid(rng, attempt, "scalpel_type2")
        spawn_params=ensure_two_distractors(spawn_params, "scalpel_type2", rng)
        spawn_params=phase3_ensure_all_5_objects_in_spawn(spawn_params, "scalpel_type2", rng)
        print(f"[EPISODE SPAWN] target={PHASE3_TARGET_OBJECT} scalpel_pose_mode={scalpel_pose_mode} params={spawn_params}")
        grid_meta_for_vis = spawn_params.get("grid", {})
        draw_spawn_grid_debug(
            stage,
            active_cell_id=int(grid_meta_for_vis.get("cell_id", -1)),
            active_target=str(grid_meta_for_vis.get("target_object", "object")),
        )
        force_episode_objects(env, spawn_params, scalpel_pose_mode)
        force_extra_distractors(env, spawn_params, "scalpel_type2")
        debug_print_extra_object_positions(env, "after_force_spawn")

        debug_print_object_positions(env, "after_force_spawn")

        print("[SETTLE] waiting after direct pose write...")
        wait_for_settle(env)
        debug_print_object_positions(env, "after_settle")
        debug_print_extra_object_positions(env, "after_settle")

        scalpel_type2_raw=get_scalpel_type2_pos_w(env)
        scalpel_center=get_scalpel_center_w(env)

        dist_obj=torch.linalg.norm((scalpel_type2_raw-scalpel_center)[:2]).item()
        if dist_obj < SPAWN_MIN_OBJ_OBJ:
            print(f"[SPAWN FAIL] too close after pose write ({dist_obj:.3f}m)"); recorder._reset(); continue

        tray_center=sample_tray_center(rng, env.device, scalpel_type2_raw, scalpel_center)

        if tray_center is None:
            print("[SPAWN] no valid tray pos"); recorder._reset(); continue

        spawn_tray(stage,tray_center)
        try:
            set_semantic_label(
                stage,
                "/World/RandomTray",
                "surgical_tray",
            )
            print("[SEMANTIC TRAY] /World/RandomTray -> surgical_tray")
        except Exception as e:
            print("[SEMANTIC TRAY WARN]", repr(e))
        # semantic labels are applied by phase3_apply_semantic_labels(stage)
        scalpel_type2_slot_w=tray_center+torch.tensor(SCALPEL_TYPE2_SLOT_OFFSET,device=env.device)
        scalpel_slot_w=tray_center+torch.tensor(SCALPEL_SLOT_OFFSET,device=env.device)
        print(f"  scalpel_type2 slot: {[round(x,4) for x in scalpel_type2_slot_w.tolist()]}")
        print(f"  scalpel slot: {[round(x,4) for x in scalpel_slot_w.tolist()]}")

        # ?? SINGLE-OBJECT PHASE: SCALPEL_TYPE2 ONLY ?????????????????????????????
        print("\n[PHASE] ScalpelType2 -> left slot | phase_id=1")
        sc_ok,sc_mz,sc_cz,sc_fp=pick_and_place_object(
            env,recorder,stage,"SCALPEL_TYPE2",3,
            SCALPEL_TYPE2_GRASP_ABOVE_TABLE,
            SCALPEL_TYPE2_BODY_OFFSET_X,SCALPEL_TYPE2_BODY_OFFSET_Y,SCALPEL_TYPE2_BODY_OFFSET_Z,
            get_scalpel_type2_pos_w,get_scalpel_type2_quat_w,scalpel_type2_slot_w,base_grip_quat)

        if not sc_ok:
            print("[PHASE FAIL] scalpel_type2 micro-lift"); recorder._reset(); continue
        if not quality_ok(recorder,"SCALPEL_TYPE2_"):
            print("[SCALPEL_TYPE2 QUALITY FAIL]"); recorder._reset(); continue

        sc_err=torch.linalg.norm((sc_fp-scalpel_type2_slot_w)[:2]).item()
        sc_ok2=sc_mz>sc_cz+0.06 and sc_err<0.09 and float(sc_fp[2])<0.12
        print(f"[SCALPEL_TYPE2 RESULT] mz={sc_mz:.4f} err={sc_err:.4f} fz={float(sc_fp[2]):.4f} ok={sc_ok2}")

        if not sc_ok2:
            print("[PHASE FAIL] scalpel_type2 place"); recorder._reset(); continue

        T=len(recorder.actions)
        if T>900:
            print(f"[QUALITY] {T}>900 steps"); recorder._reset(); continue

        success=sc_ok2
        meta={
            "task_mode":"scalpel_type2_only",
            "target_object":"scalpel_type2",
            "phase_id":1,
            "attempt":attempt,
            "scalpel_pose_mode":scalpel_pose_mode,
            "scalpel_type2_spawn":json.dumps(spawn_params["scalpel_type2"]),
            "scalpel_spawn":json.dumps(spawn_params["scalpel"]),
            "sc_mz":sc_mz,
            "sc_err":sc_err,
            "total_steps":T,
            "task":args_cli.task,
        }
        print(f"\n[RESULT] success={success} steps={T}")


        pick_out_dir = os.path.join(args_cli.out_dir, "pick_policy", "scalpel_type2")
        place_out_dir = os.path.join(args_cli.out_dir, "place_policy", "scalpel_type2")

        grid_meta = spawn_params.get("grid", {})
        meta.update({
            "grid_cell_id": int(grid_meta.get("cell_id", -1)),
            "grid_row": int(grid_meta.get("row", -1)),
            "grid_col": int(grid_meta.get("col", -1)),
            "grid_x": float(grid_meta.get("x", 0.0)),
            "grid_y": float(grid_meta.get("y", 0.0)),
            "target_yaw_deg": float(grid_meta.get("target_yaw_deg", 0.0)),
            "requested_num_distractors": int(grid_meta.get("requested_num_distractors", REQUESTED_NUM_DISTRACTORS)),
            "actual_num_distractors": int(grid_meta.get("actual_num_distractors", 1)),
            "distractor_note": "three distractors configured for this target",
            "distractor_objects": "scissor,scalpel,love_retractor",
        })

        ok_pick = save_realcompat_segment(recorder, saved_count, "pick", pick_out_dir, success, "scalpel_type2", meta=meta)
        ok_place = save_realcompat_segment(recorder, saved_count, "place", place_out_dir, success, "scalpel_type2", meta=meta)

        if ok_pick and ok_place:
            saved_count+=1; print(f"[SAVE SPLIT] {saved_count}/{target_success} -> pick+place")
            phase3_prune_outputs_by_record_mode(str(getattr(args_cli, "out_dir", globals().get("PHASE3_OUT_DIR", "datasets/phase3_out"))))
            if saved_count%args_cli.save_every==0:
                save_progress(args_cli.out_dir,saved_count,attempt)

    compute_and_save_realcompat_norm_stats(os.path.join(args_cli.out_dir, "pick_policy", "scalpel_type2"))
    compute_and_save_realcompat_norm_stats(os.path.join(args_cli.out_dir, "place_policy", "scalpel_type2"))
    print("[DONE]")
    print("[RECORD_MODE FINAL PRUNE CALL]")
    phase3_prune_outputs_by_record_mode(str(getattr(args_cli, "out_dir", globals().get("PHASE3_OUT_DIR", "datasets/phase3_out"))))
    env.close()
    simulation_app.close()

if __name__=="__main__":
    main()

'''
PS C:\IsaacLab> .\_isaac_sim\python.bat .\scripts\custom\pickplace_dualobj.py --task "Isaac-Lift-Cube-Franka-IK-Abs-v0" --episodes 50
'''
