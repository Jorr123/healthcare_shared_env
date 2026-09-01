
# Auto patch helper for Phase3 recorders.
# Uses phase3_camera_tuning.py as the single camera source of truth.

import importlib.util
from pathlib import Path
import json
import numpy as np

PHASE3_EXTRA_CAMERA_NAMES = ("cam_top", "cam_left", "cam_right", "cam_tray")
PHASE3_ALL_CAMERA_VIEWS = ("front", "grip_b", "cam_top", "cam_left", "cam_right", "cam_tray")

def phase3_load_camera_tuning():
    cfg_path = Path(__file__).with_name("phase3_camera_tuning.py")
    spec = importlib.util.spec_from_file_location("phase3_camera_tuning", str(cfg_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def phase3_apply_final_cameras_to_env_cfg(env_cfg):
    """
    Apply tuned cameras to recorder env_cfg.

    Important:
    - key 'camera' is the front camera.
    - grip_cam_b is intentionally NOT overwritten here.
    - extra static cameras are cam_top/cam_left/cam_right/cam_tray.
    """
    from isaaclab.sensors import CameraCfg
    import isaaclab.sim as sim_utils
    from phase3_shared_env_cfg import WORKSPACE

    mod = phase3_load_camera_tuning()
    cams = getattr(mod, "PHASE3_CAMERAS")
    width = int(getattr(mod, "CAMERA_WIDTH", 224))
    height = int(getattr(mod, "CAMERA_HEIGHT", 224))
    data_types = list(getattr(mod, "CAMERA_DATA_TYPES", ["rgb", "distance_to_image_plane", "semantic_segmentation"]))

    apply_names = ("camera", "grip_cam_b") + PHASE3_EXTRA_CAMERA_NAMES
    robot_attached = {"grip_cam_b"}

    def resolved_pos(name, pos):
        # Static cameras are children of env_0, so their tuned positions are
        # workspace-local coordinates and must follow the shared translation.
        # Robot-mounted cameras must retain their link-local offsets.
        if name in robot_attached:
            return tuple(pos)
        return tuple(float(pos[i]) + float(WORKSPACE.offset[i]) for i in range(3))

    for name in apply_names:
        if name not in cams:
            raise RuntimeError(f"Missing camera '{name}' in phase3_camera_tuning.py")

        c = cams[name]
        setattr(
            env_cfg.scene,
            name,
            CameraCfg(
                prim_path=c["prim_path"],
                spawn=sim_utils.PinholeCameraCfg(
                    focal_length=float(c.get("focal_length", 16.0)),
                    horizontal_aperture=float(c.get("horizontal_aperture", 20.955)),
                    clipping_range=tuple(c.get("clipping_range", (0.01, 10.0))),
                ),
                width=width,
                height=height,
                data_types=data_types,
                update_period=0,
                offset=CameraCfg.OffsetCfg(
                    pos=resolved_pos(name, c["pos"]),
                    rot=tuple(c["rot"]),
                ),
            ),
        )

    print("[PHASE3 CAMERA TUNING APPLIED]")
    print("  workspace_offset=", WORKSPACE.offset)
    print("  camera/front =", resolved_pos("camera", cams["camera"]["pos"]), cams["camera"]["rot"])
    for name in PHASE3_EXTRA_CAMERA_NAMES:
        print(f"  {name:9s} =", resolved_pos(name, cams[name]["pos"]), cams[name]["rot"])
    print("  grip_cam_b   =", cams["grip_cam_b"]["pos"], cams["grip_cam_b"]["rot"])
    return env_cfg

def phase3_safe_semantic(cam_obj, h, w, cam_name, semantic_fn=None):
    if semantic_fn is None:
        return np.zeros((h, w), dtype=np.uint16)
    try:
        out = semantic_fn(cam_obj, h, w, cam_name=cam_name)
        if out is None:
            return np.zeros((h, w), dtype=np.uint16)
        return out
    except Exception:
        return np.zeros((h, w), dtype=np.uint16)


def phase3_dump_runtime_alignment(tag="recorder"):
    """
    Runtime USD alignment audit.
    Prints camera prim transforms and likely robot/table/floor/tray/object prims.
    """
    try:
        import omni.usd
        from pxr import UsdGeom
    except Exception as e:
        print("[ALIGN AUDIT WARN] import failed:", repr(e))
        return

    stage = omni.usd.get_context().get_stage()

    exact_paths = [
        "/World/envs/env_0/Camera",
        "/World/envs/env_0/Robot",
        "/World/envs/env_0/Robot/panda_hand/GripCamB_Final",
        "/World/envs/env_0/CamTop",
        "/World/envs/env_0/CamLeft",
        "/World/envs/env_0/CamRight",
        "/World/envs/env_0/CamTray",
        "/World/envs/env_0/Object",
        "/World/envs/env_0/scalpel",
        "/World/envs/env_0/scissor",
        "/World/envs/env_0/love_retractor",
        "/World/envs/env_0/kelly",
        "/World/envs/env_0/scalpel_type2",
        "/World/envs/env_0/Tray",
        "/World/envs/env_0/Table",
        "/World/envs/env_0/GroundPlane",
    ]

    print("")
    print("=" * 110)
    print(f"[PHASE3 RUNTIME ALIGNMENT AUDIT] tag={tag}")
    print("=" * 110)

    print("\n[CAMERA TUNING SOURCE]")
    try:
        mod = phase3_load_camera_tuning()
        cams = getattr(mod, "PHASE3_CAMERAS")
        for name in ["camera", "grip_cam_b", "cam_top", "cam_left", "cam_right", "cam_tray"]:
            c = cams.get(name)
            if c is None:
                print(f"  {name:12s} MISSING in tuning")
            else:
                print(f"  {name:12s} prim={c['prim_path']} pos={c['pos']} rot={c['rot']}")
    except Exception as e:
        print("[WARN] cannot print tuning:", repr(e))

    def dump_prim(path, label=None):
        prim = stage.GetPrimAtPath(path)
        if not prim.IsValid():
            print(f"  [MISS] {label or path:20s} {path}")
            return

        try:
            xf = UsdGeom.Xformable(prim)
            local = xf.GetLocalTransformation()
            world = UsdGeom.XformCache().GetLocalToWorldTransform(prim)

            lt = local.ExtractTranslation()
            lq = local.ExtractRotationQuat()
            li = lq.GetImaginary()

            wt = world.ExtractTranslation()
            wq = world.ExtractRotationQuat()
            wi = wq.GetImaginary()

            print(f"  [OK] {label or path:20s}")
            print(f"       path  = {path}")
            print(f"       local pos = ({float(lt[0]): .6f}, {float(lt[1]): .6f}, {float(lt[2]): .6f})")
            print(f"       local rot = ({float(lq.GetReal()): .8f}, {float(li[0]): .8f}, {float(li[1]): .8f}, {float(li[2]): .8f})")
            print(f"       world pos = ({float(wt[0]): .6f}, {float(wt[1]): .6f}, {float(wt[2]): .6f})")
            print(f"       world rot = ({float(wq.GetReal()): .8f}, {float(wi[0]): .8f}, {float(wi[1]): .8f}, {float(wi[2]): .8f})")
        except Exception as e:
            print(f"  [ERR] {label or path:20s} {path}: {repr(e)}")

    print("\n[EXACT PATHS]")
    for p in exact_paths:
        dump_prim(p, p.split("/")[-1])

    print("\n[SEARCH CANDIDATES: table/tray/floor/ground/robot/camera/object]")
    keywords = ["table", "tray", "floor", "ground", "robot", "camera", "cam", "object", "scalpel", "scissor", "kelly", "love"]
    hits = []
    for prim in stage.Traverse():
        p = str(prim.GetPath())
        low = p.lower()
        if "/world/envs/env_0" not in low:
            continue
        if any(k in low for k in keywords):
            hits.append(p)

    for p in hits[:120]:
        print(" ", p)
    if len(hits) > 120:
        print(f"  ... {len(hits)-120} more")

    print("=" * 110)
    print("")
