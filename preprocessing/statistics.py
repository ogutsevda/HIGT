import os
import openslide
import pandas as pd


def generate_pl_bm(WSI_dir, save_dir, base_patch_size, target_mag):
    process_list = {}
    base_mag_csv = {"slide_path": [], "base_mag": []}

    for WSI in os.listdir(WSI_dir):
        slide = openslide.OpenSlide(os.path.join(WSI_dir, WSI))
        wsi_name = WSI.split("/")[-1]

        print(f"Processing {wsi_name}...")

        try:
            mppx_value = float(slide.properties["openslide.mpp-x"])
            mppy_value = float(slide.properties["openslide.mpp-y"])
        except:
            continue

        if mppx_value == None or mppy_value == None:
            continue

        if 0 < mppx_value < 0.26 and 0 < mppy_value < 0.26:
            base_mag = 40
        elif 0.26 <= mppx_value < 0.52 and 0.26 <= mppy_value < 0.52:
            base_mag = 20
        else:
            raise ValueError(f"Unknown magnification for slide {WSI}!")

        target_min_patch_size = int(base_patch_size * (base_mag / target_mag))

        if target_min_patch_size not in process_list:
            process_list[target_min_patch_size] = [wsi_name]
        else:
            process_list[target_min_patch_size].append(wsi_name)

        base_mag_csv["slide_path"].append(WSI)
        base_mag_csv["base_mag"].append(base_mag)

        df = pd.DataFrame(base_mag_csv)
        df.to_csv(save_dir + f"bm.csv")

        for k in process_list.keys():
            df = pd.DataFrame({"slide_id": process_list[k]})
            df.to_csv(save_dir + f"pl_mag{target_mag}x_patch{base_patch_size}_{k}.csv")


generate_pl_bm(
    WSI_dir=os.path.join(os.getcwd(), "../../../TCGA/BRCA/slides"),
    save_dir=os.path.join(os.getcwd(), "../BRCA_images_todel/csv/"),
    base_patch_size=512,
    target_mag=5,
)

generate_pl_bm(
    WSI_dir=os.path.join(os.getcwd(), "../../../TCGA/BRCA/slides"),
    save_dir=os.path.join(os.getcwd(), "../BRCA_images_todel/csv/"),
    base_patch_size=512,
    target_mag=10,
)
