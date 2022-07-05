from argparse import ArgumentParser
from multiprocessing import Pool
from os import makedirs, path, sep, walk
from pathlib import Path

import cv2
import imageio
import numpy as np
import pandas as pd
import pydicom
from logger import logger
from pydicom.dataset import FileDataset
from pydicom.multival import MultiValue


def _correct_image_color_space(dcm) -> np.ndarray:
    """Corrects the image's color space and returns the numpy array

    Args:
        dcm (FileDataset): The dicom filedataset

    Returns:
        np.ndarray: The corrected image in np.uint16
    """

    def _get_lut_value(dicom_file, property):
        """
        https://github.com/pydicom/pydicom/issues/892
        If this function doesn't get called
        we would have problem with MultiValue and float
        """
        value = dicom_file.get(property, None)
        if type(value) is MultiValue:
            value = value[0]

        return value

    img = dcm.pixel_array.astype(np.int64)

    pmi = _get_lut_value(dcm, "PhotometricInterpretation")
    wc = _get_lut_value(dcm, "WindowCenter")
    ww = _get_lut_value(dcm, "WindowWidth")
    rs = _get_lut_value(dcm, "RescaleSlope")
    ri = _get_lut_value(dcm, "RescaleIntercept")

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


def check_axial_image(dcm: FileDataset):
    if "ImageType" in dcm:
        return "AXIAL" in dcm.ImageType or (
            "MPR" in dcm.ImageType and "Ax" in dcm.SeriesDescription
        )
    if "ImageOrientationPatient" in dcm:
        return dcm.ImageOrientationPatient == [1, 0, 0, 0, 1, 0]

    return False


def generate_image_file(dcm_file: Path, save_file: Path, spacing):
    try:
        logger.info(f"reading {dcm_file}")
        dcm = pydicom.read_file(dcm_file)
        if check_axial_image(dcm):
            img = _correct_image_color_space(dcm)
            logger.info(f"saving  {save_file}")
            # if dcm.Rows != 512 or dcm.Columns != 512:
            # logger.warning(
            # f"found dicom image {dcm_file} with size {dcm.Rows},{dcm.Columns}"
            # )

            resized = cv2.resize(img, (512, 512)).astype(np.uint16)
            imageio.imwrite(save_file, resized)
            spacing_x, spacing_y = dcm.PixelSpacing
            spacing.append(
                {"file_name": save_file.name, "x": spacing_x, "y": spacing_y}
            )

    except Exception:
        logger.error(f"Error Happened in file {dcm_file}", exc_info=True)


def _check_file(dcm_path, dcm_pref, save_dir):

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
    cnts = pool.starmap(_check_file, [(x, args.pref, args.save_dir) for x in dcm_paths])
    pool.close()

    print(f"Found {sum(cnts)} spots.")
