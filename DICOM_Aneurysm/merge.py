"""
Convert three images to a single three-channel image for improving performance
You will pass a complete folder and it will convert it for you in-place. So you have to make a copy for the folder.
"""

from operator import concat
from pathlib import Path
from tkinter import W

import cv2
import numpy as np
import typer
import yaml
from logger import logger

app = typer.Typer(name="Image Merger", add_completion=False)


def read_image(img_path: Path):
    image = cv2.imread(str(img_path), 0)
    if len(image.shape) != 2:
        logger.warning("file {img_path} has shape {image.shape}")
    return image


def convert_folder_images_to_3d(folder_path: str):
    folder_path = Path(folder_path)

    patients = set()
    for file in folder_path.iterdir():
        patients.add(file.name.split("_")[0])

    for patient in patients:
        logger.info(f"Processing Patient {patient}")

        previous_file = None
        pre_previous_file = None

        files = sorted(folder_path.glob(f"{patient}*"))
        for file in files:
            if pre_previous_file is not None and previous_file is not None:
                logger.info(f"Pre-Previous file: {pre_previous_file}")
                logger.info(f"Previous file:     {previous_file}")
                logger.info(f"Current file:      {file}")

                pre_previous_image = read_image(pre_previous_file)
                previous_image = read_image(previous_file)
                image = read_image(file)

                concat_image = np.dstack([pre_previous_image, previous_image, image])
                cv2.imwrite(str(previous_file), concat_image)
                logger.info(f"saved into {previous_file}")

            pre_previous_file = previous_file
            previous_file = file

        files[0].unlink()
        logger.info(f"removed file {files[0]}")
        files[-1].unlink()
        logger.info(f"removed file {files[-1]}")


@app.command()
def main(yolo_dataset_file: str):
    """
    here you should pass a yaml file which contains path to training, val and test folders
    """
    try:
        yolo_dataset_file = Path(yolo_dataset_file)
        content = yolo_dataset_file.read_text()

        dataset = yaml.safe_load(content)
        if "train" in dataset:
            convert_folder_images_to_3d(dataset["train"])
        if "val" in dataset:
            convert_folder_images_to_3d(dataset["val"])
        if "test" in dataset:
            convert_folder_images_to_3d(dataset["test"])
    except Exception:
        logger.error("Error", exc_info=True)


if __name__ == "__main__":
    app()
