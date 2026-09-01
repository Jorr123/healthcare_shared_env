# Phase 3 Team Data Generation

This repository is the shared Phase-3 project for surgical-instrument data
generation in Isaac Lab. It was cleaned from `rheo2_copy` so both team members
can use the same environment, assets, spawn rules, object profiles, and FSM.

Both collectors now run the same scene, five-object spawn logic, object profiles,
14-stage FSM, waypoints, and success checks. They split only at the controller
and recorder adapters because the two training formats require different actions
and observations.

The OpenVLA workflow records 7D relative actions:

```text
[delta_x, delta_y, delta_z,
 delta_axis_angle_x, delta_axis_angle_y, delta_axis_angle_z,
 binary_gripper]
```

The teammate workflow records the original 8D absolute action:

```text
[x, y, z, qw, qx, qy, qz, binary_gripper]
```

The gripper value is always `+1` for open or `-1` for closed in both outputs.
The OpenVLA main image is RGB at 224x224; its wrist view is 448x336. The
teammate output keeps all six original 448x336 RGB-D-semantic cameras.

## Repository structure

```text
phase3_team/
├── configs/
│   ├── scene_cfg.py              Shared scene bridge and observations
│   └── camera_cfg.py             Dedicated 224x224 OpenVLA camera
├── core/
│   ├── contract.py               Shared paths and workspace contract
│   ├── spawn.py                  Five-object spawn sampling
│   ├── object_profiles.py        Per-object grasp and timing values
│   ├── fsm.py                    One FSM used for all five objects
│   ├── actions.py                Relative 7D and absolute 8D adapters
│   └── runner.py                 Simulator collection loop
├── recorders/
│   ├── openvla_hdf5_recorder.py  OpenVLA HDF5 format
│   ├── teammate_hdf5_recorder.py Original teammate HDF5 format
│   ├── hdf5_validation.py        Automatic output-contract checks
│   └── contract.py               Recorder step interface
├── scripts/
│   ├── collect_openvla.py        Shared OpenVLA entry point
│   └── collect_teammate.py       Shared teammate-format entry point
├── tests/
│   └── test_phase3_team_sync.py
└── teammate_env/
    ├── assets/                    One authoritative shared asset path
    ├── shared_layout.json         Robot, table, room, and workspace layout
    ├── phase3_shared_env_cfg.py   Original teammate environment config
    ├── phase3_camera_tuning.py    Original six-camera settings
    └── phase3_grid_split_*_recorder.py
```

`teammate_env/` keeps the original teammate release and recorder files as the
reference for assets, layout, camera settings, and data compatibility. The two
commands above do not execute those five old procedural recorder scripts; both
call `core/runner.py` and `core/fsm.py`. New shared behavior belongs in
`configs/`, `core/`, and `recorders/`. Generated datasets never belong in Git.

## Requirements

- The same Isaac Lab and Isaac Sim version used by the team
- Python packages already provided by that environment
- Isaac Lab tasks named `Isaac-Lift-Cube-Franka-IK-Rel-v0` and
  `Isaac-Lift-Cube-Franka-IK-Abs-v0`

The repository does not install Isaac Lab. Run the scripts through the
`isaaclab.sh` launcher from an existing IsaacLab checkout.

## Run the shared OpenVLA collector

From the IsaacLab repository root, use the absolute or relative path to this
cloned repository:

```bash
./isaaclab.sh -p /path/to/phase3_team/scripts/collect_openvla.py \
  --target scalpel \
  --episodes 1 \
  --record-skill both \
  --output-dir /workspace/isaaclab/datasets/phase3_openvla_pilot
```

Use `--headless` only after checking one visible episode. Valid targets are:

```text
scalpel
scissor
love_retractor
kelly
scalpel_type2
```

## Run the teammate-format collector

This uses the same shared FSM and spawn sampled by the OpenVLA command, while
writing the teammate's original split-policy HDF5 structure.

```bash
./isaaclab.sh -p /path/to/phase3_team/scripts/collect_teammate.py \
  --target scalpel \
  --episodes 1 \
  --record-mode both \
  --output-dir /workspace/isaaclab/datasets/phase3_teammate_pilot
```

For compatibility, the positional target and old option spellings also work.
The output is placed under `pick_policy/<target>/` and
`place_policy/<target>/`. Each episode contains 18D state, 8D absolute action,
stage labels, debug ground truth, and six RGB-D-semantic views. A dataset-level
`norm_stats.json` is written into each requested skill directory.

These files are much larger than OpenVLA episodes because they contain six
camera streams. Plan storage before collecting many episodes.

## What is shared and what stays separate

```text
shared scene + assets + spawn + object profile + FSM + success checks
                                  |
                    desired world-frame EE pose
                         /                    \
       relative 7D OpenVLA adapter      absolute 8D teammate adapter
                  |                              |
       OpenVLA 224 RGB HDF5         original six-camera teammate HDF5
```

Do not create separate object-specific FSM copies. Object differences belong in
`core/object_profiles.py`; changes to motion stages belong in `core/fsm.py`.

## Run fast tests

These tests do not start Isaac Sim:

```bash
python3 -m pytest
```

They check asset resolution, one-target scene mapping, 20-cell target coverage,
five-object spacing, shared FSM stages, segment boundaries, and the binary
gripper contract. Every saved HDF5 file is also checked automatically for its
required dimensions, camera streams, action type, and data types.

## Team workflow

1. Pull the latest `main` branch before making changes.
2. Create a short branch for one change.
3. Change shared behavior only in `configs/`, `core/`, or `recorders/`.
4. Run `python3 -m pytest`.
5. Run one visible simulator episode for the affected object.
6. Open a pull request and ask the other team member to review it.
7. Do not commit datasets, checkpoints, videos, cache files, or generated HDF5 files.

When changing the scene, camera, spawn logic, FSM, or object profiles, both team
members should use the same commit hash for their next data collection run.

## Before making the GitHub repository public

Confirm that the team has permission to redistribute every file in
`teammate_env/assets/`. If that permission is only for the project team, use a
private GitHub repository.
