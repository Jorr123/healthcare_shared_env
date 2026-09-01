import json
import os

import h5py
import numpy as np
import torch

from recorders.contract import RecorderStep
from recorders.hdf5_validation import validate_openvla_episode


class OpenVLAHDF5Recorder:
    """Write the shared OpenVLA RGB, wrist RGB, proprio, and 7D action schema."""
    def __init__(
        self,
        output_dir="data_collection",
        task_description="Pick up the Scalpel and place it on the tray",
    ):
        """
        Initializes the data recorder.
        output_dir: Folder where HDF5 files will be saved.
        task_description: The text instruction for OpenVLA (e.g., "Put the peg in the hole").
        """
        self.output_dir = output_dir
        self.task_desc = task_description
        os.makedirs(self.output_dir, exist_ok=True)

        # Buffers to hold data for the current episode.
        self.reset_buffers()

    def reset_buffers(self):
        self.images = []
        self.actions = []
        self.proprio = []
        self.wrist_images = []

    def add_step(self, step: RecorderStep):
        """Record one relative-action OpenVLA timestep."""
        obs_dict = step.observation
        action_tensor = step.action
        img_tensor = obs_dict["policy"]["image"][0]  # Take env 0.

        if isinstance(img_tensor, torch.Tensor):
            img_np = img_tensor.cpu().numpy()
        else:
            img_np = img_tensor

        if img_np.dtype == np.float32 or img_np.max() <= 1.5:
            img_np = (img_np * 255).astype(np.uint8)

        wrist_image_tensor = obs_dict["policy"]["wrist_image"][0]
        if isinstance(wrist_image_tensor, torch.Tensor):
            wrist_img_np = wrist_image_tensor.cpu().numpy()
        else:
            wrist_img_np = wrist_image_tensor

        if wrist_img_np.dtype == np.float32 or wrist_img_np.max() <= 1.5:
            wrist_img_np = (wrist_img_np * 255).astype(np.uint8)

        act_np = action_tensor[0].cpu().numpy()

        prop_tensor = obs_dict["policy"]["proprio"][0]
        if isinstance(prop_tensor, torch.Tensor):
            prop_np = prop_tensor.cpu().numpy()
        else:
            prop_np = prop_tensor

        self.images.append(img_np)
        self.wrist_images.append(wrist_img_np)
        self.actions.append(act_np)
        self.proprio.append(prop_np)

    def save_episode(self, ep, metadata=None):
        """
        Saves the currently buffered episode to an HDF5 file.

        Args:
            ep: Episode identifier used in the filename.
            metadata: Extra shared contract attributes for the HDF5 root.

        Returns:
            The saved filename, or ``None`` when the buffer is empty.
        """
        if len(self.images) == 0:
            print("[Recorder] Buffer empty, nothing to save.")
            return None

        os.makedirs(self.output_dir, exist_ok=True)
        filename = os.path.join(self.output_dir, f"episode_{ep}.h5")

        img_data = np.array(self.images)
        wrist_img_data = np.array(self.wrist_images)
        act_data = np.array(self.actions)
        prop_data = np.array(self.proprio)

        with h5py.File(filename, "w") as h5_file:
            h5_file.attrs["language_instruction"] = self.task_desc
            for key, value in (metadata or {}).items():
                h5_file.attrs[key] = (
                    value
                    if isinstance(value, (str, int, float, bool))
                    else json.dumps(value)
                )
            h5_file.create_dataset(
                "observations/images",
                data=img_data,
                compression="gzip",
            )
            h5_file.create_dataset(
                "observations/wrist_images",
                data=wrist_img_data,
                compression="gzip",
            )
            h5_file.create_dataset("observations/proprio", data=prop_data)
            h5_file.create_dataset("actions", data=act_data)

            if act_data.ndim != 2 or act_data.shape[1] != 7:
                raise RuntimeError(
                    f"OpenVLA action contract violated in {filename}: shape={act_data.shape}"
                )
            if not np.isin(act_data[:, 6], (-1.0, 1.0)).all():
                raise RuntimeError(f"Non-binary gripper action written to {filename}")
            if img_data.ndim != 4 or img_data.shape[1:] != (224, 224, 3):
                raise RuntimeError(
                    f"OpenVLA image contract violated in {filename}: shape={img_data.shape}"
                )

        validate_openvla_episode(filename)
        print(f"[Recorder] Saved and validated episode with {len(self.images)} steps to: {filename}")
        self.reset_buffers()
        return filename
