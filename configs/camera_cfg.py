"""OpenVLA policy camera configuration.

The teammate's six reference cameras remain authoritative in
``teammate_env/phase3_camera_tuning.py``.  This module owns only the extra
224x224 RGB view used by the OpenVLA recorder.
"""

from __future__ import annotations

import torch

import isaaclab.sim as sim_utils
import isaaclab.utils.math as math_utils
from isaaclab.sensors import CameraCfg


OPENVLA_CAMERA_NAME = "openvla_camera"
OPENVLA_CAMERA_WIDTH = 224
OPENVLA_CAMERA_HEIGHT = 224
OPENVLA_CAMERA_FOCAL_LENGTH = 20.0

# Workspace-local position and look-at point.  The view includes the five
# object grid, gripper, and tray without spending most pixels on empty space.
OPENVLA_CAMERA_LOCAL_POS = (1.14, 0.03, 0.62)
OPENVLA_CAMERA_LOCAL_LOOK_AT = (0.49, 0.03, 0.06)


def openvla_camera_cfg(workspace_offset: tuple[float, float, float]) -> CameraCfg:
    """Build the dedicated square RGB camera used by the OpenVLA policy."""

    eye = torch.tensor(
        [[OPENVLA_CAMERA_LOCAL_POS[i] + float(workspace_offset[i]) for i in range(3)]],
        dtype=torch.float32,
    )
    target = torch.tensor(
        [[OPENVLA_CAMERA_LOCAL_LOOK_AT[i] + float(workspace_offset[i]) for i in range(3)]],
        dtype=torch.float32,
    )
    rotation = math_utils.quat_from_matrix(
        math_utils.create_rotation_matrix_from_view(eye, target, up_axis="Z")
    )[0]
    return CameraCfg(
        prim_path="{ENV_REGEX_NS}/OpenVLACamera",
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=OPENVLA_CAMERA_FOCAL_LENGTH,
            horizontal_aperture=20.955,
            clipping_range=(0.01, 10.0),
        ),
        width=OPENVLA_CAMERA_WIDTH,
        height=OPENVLA_CAMERA_HEIGHT,
        data_types=["rgb"],
        update_period=0,
        offset=CameraCfg.OffsetCfg(
            pos=tuple(float(value) for value in eye[0].tolist()),
            rot=tuple(float(value) for value in rotation.tolist()),
            convention="opengl",
        ),
    )
