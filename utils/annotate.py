"""
This file gets annotation and image folder  and draws annotation over images
"""

from pathlib import Path

import cv2
import imageio
import numpy as np

from logger import logger


def process_needed_files(png_dir: Path, annotations):
    for file_annotation in annotations:
        file_name, coordinates = file_annotation
        png_file = png_dir / (file_name.split("\\")[-1] + ".png")
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

    # class label is always zero
    yolo_file.write_text(
        f"0 {b_center_x:.7f} {b_center_y:.7f} {b_width:.7f} {b_height:.7f}"
    )
    logger.info(f"write yolo {yolo_file}")


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
        _generate_yolo(
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

    annotated_dir = image_path.parent.parent / ("bbox" if bbox else "annotated")
    if not annotated_dir.exists():
        annotated_dir.mkdir(exist_ok=True)

    annotated_path = annotated_dir / image_path.name
    imageio.imwrite(annotated_path, image)
    logger.info(f"saved annotated {annotated_path}")

    return annotated_dir
