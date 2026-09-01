"""Public teammate recorder API.

The legacy five-script launcher was replaced by one shared-FSM recorder. The
original scripts remain under ``teammate_env`` only as compatibility references.
"""

from recorders.teammate_hdf5_recorder import (
    TeammateHDF5Recorder,
    write_dataset_norm_stats,
)

__all__ = ["TeammateHDF5Recorder", "write_dataset_norm_stats"]
