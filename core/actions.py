"""Action adapters for one shared FSM and two policy contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

import torch

import isaaclab.utils.math as math_utils


class ActionAdapter(Protocol):
    """Convert a world-frame FSM target into the environment action."""

    action_dim: int
    action_type: str

    def make_action(
        self,
        env: Any,
        current_pos_w: torch.Tensor,
        current_quat_w: torch.Tensor,
        desired_pos_w: torch.Tensor,
        desired_quat_w: torch.Tensor,
        gripper: float,
    ) -> torch.Tensor: ...


@dataclass(frozen=True)
class RelativeOpenVLAActionAdapter:
    """Rheo2/OpenVLA delta XYZ + delta axis-angle + binary grip."""

    kp: float = 1.0
    kp_rot: float = 3.1
    max_delta: float = 0.06
    max_rot_delta: float = 0.20

    action_dim: int = 7
    action_type: str = "relative_base_xyz_axis_angle_binary_gripper"

    def make_action(
        self,
        env,
        current_pos_w,
        current_quat_w,
        desired_pos_w,
        desired_quat_w,
        gripper,
    ) -> torch.Tensor:
        base_quat = env.scene["robot"].data.root_quat_w[0:1]
        pos_world = (desired_pos_w - current_pos_w).unsqueeze(0)
        pos_base = math_utils.quat_apply_inverse(base_quat, pos_world) * self.kp
        pos_base = torch.clamp(pos_base, -self.max_delta, self.max_delta)

        quat_error_world = math_utils.quat_mul(
            desired_quat_w.unsqueeze(0),
            math_utils.quat_inv(current_quat_w.unsqueeze(0)),
        )
        rot_world = math_utils.axis_angle_from_quat(quat_error_world)
        rot_base = math_utils.quat_apply_inverse(base_quat, rot_world) * self.kp_rot
        magnitude = torch.linalg.norm(rot_base, dim=-1, keepdim=True)
        rot_base = rot_base * torch.clamp(
            self.max_rot_delta / (magnitude + 1.0e-9),
            max=1.0,
        )
        grip = torch.full((env.num_envs, 1), float(gripper), device=env.device)
        return torch.cat((pos_base, rot_base, grip), dim=-1)


@dataclass(frozen=True)
class AbsoluteTeammateActionAdapter:
    """Original teammate XYZ + WXYZ quaternion + gripper action in base frame."""

    action_dim: int = 8
    action_type: str = "absolute_pose_quat_gripper_8d_baseframe"

    def make_action(
        self,
        env,
        current_pos_w,
        current_quat_w,
        desired_pos_w,
        desired_quat_w,
        gripper,
    ) -> torch.Tensor:
        del current_pos_w, current_quat_w
        robot = env.scene["robot"]
        base_pos_w = robot.data.root_pos_w[0:1]
        base_quat_w = robot.data.root_quat_w[0:1]
        desired_pos_b = math_utils.quat_apply_inverse(
            base_quat_w,
            desired_pos_w.reshape(1, 3) - base_pos_w,
        )
        desired_quat_b = math_utils.quat_mul(
            math_utils.quat_inv(base_quat_w),
            desired_quat_w.reshape(1, 4),
        )
        grip = torch.full((env.num_envs, 1), float(gripper), device=env.device)
        return torch.cat((desired_pos_b, desired_quat_b, grip), dim=-1)
