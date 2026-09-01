
CAMERA_WIDTH  = 448
CAMERA_HEIGHT = 336
CAMERA_DATA_TYPES = ["rgb", "distance_to_image_plane", "semantic_segmentation"]

PHASE3_CAMERAS = {
    "camera": {
        "prim_path": "{ENV_REGEX_NS}/Camera",
        "focal_length": 16.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.01, 10.0),
        "pos": (1.256523, 0.000000, 0.297649),
        "rot": (-0.39384708, 0.57984880, 0.58908579, -0.40204201),
    },

    "grip_cam_b": {
        "prim_path": "{ENV_REGEX_NS}/Robot/panda_hand/GripCamB_Final",
        "focal_length": 14.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.001, 2.0),
        "pos": (0.061365, 0.017054, 0.040467),
        "rot": (-0.64681794, 0.15352391, 0.25956301, -0.70048840),
    },

    "cam_top": {
        "prim_path": "{ENV_REGEX_NS}/CamTop",
        "focal_length": 16.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.01, 10.0),
        "pos": (0.510759, -0.024618, 1.243130),
        "rot": (-0.00625446, 0.70707912, 0.70707912, -0.00625446),
    },

    # From your GUI CamLeft, converted to IsaacLab CameraCfg rot convention
    "cam_left": {
        "prim_path": "{ENV_REGEX_NS}/CamLeft",
        "focal_length": 16.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.01, 10.0),
        "pos": (0.349634, 0.638153, 0.779947),
        "rot": (-0.00414037, 0.00127212, -0.95588456, 0.29371064),
    },

    # From your GUI CamRight, converted to IsaacLab CameraCfg rot convention
    "cam_right": {
        "prim_path": "{ENV_REGEX_NS}/CamRight",
        "focal_length": 16.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.01, 10.0),
        "pos": (0.301181, -0.669862, 0.779950),
        "rot": (0.29903149, -0.95411975, -0.00113561, -0.01530929),
    },

    "cam_tray": {
        "prim_path": "{ENV_REGEX_NS}/CamTray",
        "focal_length": 16.0,
        "horizontal_aperture": 20.955,
        "clipping_range": (0.01, 10.0),
        "pos": (0.340000, -0.190622, 0.882957),
        "rot": (0.00503358, 0.70555958, 0.70859880, -0.00693478),
    },
}
