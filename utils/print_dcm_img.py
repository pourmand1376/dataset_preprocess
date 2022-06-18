from argparse import ArgumentParser
from multiprocessing import Pool
from os import makedirs, path, sep, walk

import cv2
import imageio
import numpy as np
import pandas as pd
import pydicom


def _correct_image_color_space(dcm) -> np.ndarray:
    """Corrects the image's color space and returns the numpy array

    Args:
        dcm (FileDataset): The dicom filedataset

    Returns:
        np.ndarray: The corrected image in np.uint16
    """

    img = dcm.pixel_array.astype(np.int64)

    pmi = dcm.get("PhotometricInterpretation", None)
    wc = dcm.get("WindowCenter", None)
    ww = dcm.get("WindowWidth", None)
    rs = dcm.get("RescaleSlope", None)
    ri = dcm.get("RescaleIntercept", None)

    # Transforming the values linearly

    if rs:
        img = img * rs

    if ri:
        img = img + ri

    # Inverting the white-black images to black-white

    x = img.astype(np.float64)

    if (ww is not None) and (wc is not None):

        if pmi == "MONOCHROME1":
            ymin, ymax = 4095, 0

        else:
            ymin, ymax = 0, 4095

        y = ((x - (wc - 0.5)) / (ww - 1) + 0.5) * (ymax - ymin) + ymin
        y = np.clip(y, min(ymin, ymax), max(ymin, ymax))
        y = np.round((y * 1.0 / 4095 * 65535), 0).astype(np.uint16)

    else:

        if pmi == "MONOCHROME1":
            y = np.amax(x) - x
        else:
            y = x

    y = np.round(y).astype(np.uint16)

    return y


def check_file(dcm_path, dcm_pref, save_dir):

    try:
        dcm = pydicom.read_file(dcm_path)
        img = _correct_image_color_space(dcm)
        sd = path.join(
            save_dir,
            dcm_path.replace(dcm_pref, "").replace(".." + sep, "").replace(sep, "@"),
        )
        makedirs(path.dirname(sd), exist_ok=True)
        imageio.imwrite(sd + ".png", cv2.resize(img, (512, 512)).astype(np.uint16))

    except Exception:
        print(f"Problem in {dcm_path}")

    return False


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("data_root")
    parser.add_argument("save_dir")
    parser.add_argument("-p", dest="pref", default="")
    parser.add_argument("-c", dest="cores", type=int, default=32)
    args = parser.parse_args()

    if path.isfile(args.data_root):
        info = pd.read_csv(args.data_root, sep=",", header=0)
        dcm_paths = info["dcm_path"].values
    else:
        dcm_paths = []
        for r, _, files in walk(args.data_root):
            for f in files:
                dcm_paths.append(path.join(r, f))

    print(f"Found {len(dcm_paths)} dcm files.")

    pool = Pool(args.cores)
    cnts = pool.starmap(check_file, [(x, args.pref, args.save_dir) for x in dcm_paths])
    pool.close()

    print(f"Found {sum(cnts)} spots.")
