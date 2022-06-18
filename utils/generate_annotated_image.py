#!/home/amir/miniconda3/envs/venv-ctscan/bin/python

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
            generate_img(png_file, coordinates)
            generate_img(png_file, coordinates, True)


def generate_img(image_path: Path, coordinates, bbox: bool = False):
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

    else:
        points = points.reshape((-1, 1, 2))
        image = cv2.polylines(image, [points], isClosed, color, thickness)

    annotated_dir = image_path.parent.parent / ("bbox" if bbox else "annotated")
    if not annotated_dir.exists():
        annotated_dir.mkdir(exist_ok=True)

    annotated_path = annotated_dir / image_path.name
    imageio.imwrite(annotated_path, image)
    logger.info(f"saved annotated {annotated_path}")
