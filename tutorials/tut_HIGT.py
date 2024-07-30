import os
import openslide
import matplotlib.pyplot as plt
from PIL import Image


def generate_pl_bm(WSI_dir, save_dir, base_patch_size, target_mag):
    import openslide, glob
    import pandas as pd

    process_list = {}
    base_mag_csv = {"slide_path": [], "base_mag": []}

    # for WSI in glob.glob(WSI_dir + "/*"):
    for WSI in os.listdir(WSI_dir):
        slide = openslide.open_slide(os.path.join(WSI_dir, WSI))
        wsi_name = WSI.split("/")[-1]
        if slide.properties.get(openslide.PROPERTY_NAME_OBJECTIVE_POWER) == None:
            continue

        base_mag = int(slide.properties.get(openslide.PROPERTY_NAME_OBJECTIVE_POWER))
        target_min_patch_size = int(base_patch_size * (base_mag / target_mag))

        # Update for process_list
        if target_min_patch_size not in process_list:
            process_list[target_min_patch_size] = [wsi_name]
        else:
            process_list[target_min_patch_size].append(wsi_name)

        # Update for bm
        base_mag_csv["slide_path"].append(WSI)
        base_mag_csv["base_mag"].append(base_mag)

        # save bm.csv
        df = pd.DataFrame(base_mag_csv)
        df.to_csv(save_dir + f"bm.csv")

        # save patch_size_i process_list.csv
        for k in process_list.keys():
            df = pd.DataFrame({"slide_id": process_list[k]})
            df.to_csv(save_dir + f"pl_mag{target_mag}x_patch{base_patch_size}_{k}.csv")


# generate_pl_bm(
#     WSI_dir=os.path.join(os.getcwd(), "../../../TCGA/BRCA/slides"),
#     save_dir=os.path.join(os.getcwd(), "../BRCA_images_todel/csv/"),
#     base_patch_size=512,
#     target_mag=5,
# )

slide_path = os.path.join(
    os.getcwd(),
    "../../../TCGA/BRCA/slides/TCGA-A8-A06N-01Z-00-DX1.E25E65F8-DFE0-47CF-9FAB-B82EE8E321F7.svs",
)
slide = openslide.OpenSlide(slide_path)

slide_dimensions = slide.dimensions
print(f"Dimensions of the slide: {slide_dimensions}")

level = 0
region = slide.read_region((0, 0), level, slide_dimensions)

region = region.convert("RGB")

plt.imshow(region)
plt.title("Whole Slide Image")
plt.axis("off")
plt.show()
