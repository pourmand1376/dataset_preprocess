"""
This file gets annotation and image folder  and draws annotation over images
"""

from pathlib import Path

import cv2
import imageio
import numpy as np
from logger import logger

from .utility import find_all_numbers_folder


def process_needed_files(png_dir: Path, annotations):
    yolo_dir = None

    img_folder = find_all_numbers_folder(png_dir.parent)
    parents_name = "_".join(str(img_folder).split("/")[-4:])
    for file_annotation in annotations:
        extended_file_name, coordinates = file_annotation
        file_name = extended_file_name.split("\\")[-1]
        file_name = f"{parents_name}_{file_name}.png"

        png_file = png_dir / file_name
        if png_file.exists():
            # uncomment below line if you want to see
            # png image with bbox on top of it
            # _ = _generate_img(png_file, coordinates)
            yolo_dir = _generate_img(png_file, coordinates, bbox=True)
        else:
            logger.warning(f"png file doesn't exists {png_file}")

    return yolo_dir


def _generate_yolo(
    image_path: Path,
    min_x: int,
    min_y: int,
    max_x: int,
    max_y: int,
    image_height: int,
    image_width: int,
):
    yolo_dir = image_path.parent.parent / "yolo"
    if not yolo_dir.exists():
        yolo_dir.mkdir(exist_ok=True)

    yolo_file = yolo_dir / image_path.name.replace(".png", ".txt")

    b_center_x = (min_x + max_x) / 2
    b_center_y = (min_y + max_y) / 2
    b_width = max_x - min_x
    b_height = max_y - min_y

    # Normalise the co-ordinates by the dimensions of the image
    b_center_x /= image_width
    b_center_y /= image_height
    b_width /= image_width
    b_height /= image_height

    if b_width <= 13 or b_height <= 13:
        logger.info(
            f"file {yolo_file} ignored since it has width={b_width}, height={b_height}"
        )
        return yolo_dir
    # class label is always zero
    yolo_file.write_text(
        f"0 {b_center_x:.7f} {b_center_y:.7f} {b_width:.7f} {b_height:.7f}"
    )
    logger.info(f"write yolo {yolo_file}")
    return yolo_dir


def _generate_img(image_path: Path, coordinates, bbox: bool = False):
    image = cv2.imread(str(image_path))

    points = []
    for coordinate in coordinates:
        x = round(float(coordinate["x"]))
        y = round(float(coordinate["y"]))

        points.append([x, y])

    points = np.array(points)

    color = (255, 255, 0)
    thickness = 1
    isClosed = False

    if bbox:
        x_values = points[:, 0]
        y_values = points[:, 1]
        min_x, max_x = x_values.min(), x_values.max()
        min_y, max_y = y_values.min(), y_values.max()
        image = cv2.rectangle(image, (min_x, min_y), (max_x, max_y), color, thickness)
        return _generate_yolo(
            image_path,
            min_x=min_x,
            min_y=min_y,
            max_x=max_x,
            max_y=max_y,
            image_width=image.shape[0],
            image_height=image.shape[1],
        )
    else:
        points = points.reshape((-1, 1, 2))
        image = cv2.polylines(image, [points], isClosed, color, thickness)

        annotated_dir = image_path.parent.parent / "annotated"
        if not annotated_dir.exists():
            annotated_dir.mkdir(exist_ok=True)

        annotated_path = annotated_dir / image_path.name
        imageio.imwrite(annotated_path, image)
        logger.info(f"saved annotated {annotated_path}")

        return annotated_dir
