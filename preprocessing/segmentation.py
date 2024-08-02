import os, h5py, glob
import numpy as np
from wsi_core.wsi_utils import save_hdf5


def generate_coords_file(source_mag_seg_path, target_mag):

    cur_mag = int(
        source_mag_seg_path.split("/")[-1]
        .split("_")[0]
        .replace("mag", "")
        .replace("x", "")
    )
    cur_patch_size = int(source_mag_seg_path.split("/")[-1].split("_")[-1])
    target_patch_size = int(cur_patch_size / int(target_mag / cur_mag))

    for h5 in glob.glob(source_mag_seg_path + "/patches/*"):
        h5_content = h5py.File(h5, "r")

        coords = h5_content["coords"][:]
        save_path = (
            "/".join(source_mag_seg_path.split("/")[:-1])
            + f"/mag{target_mag}x_patch512_{target_patch_size}/patches/"
        )

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        attr = {
            "patch_size": target_patch_size,
            "patch_level": h5_content["coords"].attrs["patch_level"],
            "downsample": h5_content["coords"].attrs["downsample"],
            "downsampled_level_dim": h5_content["coords"].attrs[
                "downsampled_level_dim"
            ],
            "level_dim": h5_content["coords"].attrs["level_dim"],
            "name": h5_content["coords"].attrs["name"],
            "save_path": save_path,
        }

        h5_content.close()
        coords_ = []
        for coord in coords:
            x, y = coord
            coords_.append([x, y])
            coords_.append([x + target_patch_size, y])
            coords_.append([x, y + target_patch_size])
            coords_.append([x + target_patch_size, y + target_patch_size])

        coords_ = np.array(coords_).astype(coords.dtype)
        unique_coords = np.unique(coords_, axis=0)

        save_hdf5(
            save_path + h5.split("/")[-1],
            {"coords": unique_coords},
            {"coords": attr},
            mode="w",
        )
