#!/home/amir/miniconda3/envs/venv-ctscan/bin/python

"""
This file gets annotation and image folder  and draws annotation over images
"""

from pathlib import Path

import cv2
import imageio
import numpy as np


def process_needed_files(png_dir: Path, annotations):
    for file_annotation in annotations:
        file_name, coordinates = file_annotation
        png_file = png_dir / (file_name.split("\\")[-1] + ".png")
        generate_img(png_file, coordinates)


def generate_img(image_path: Path, coordinates):
    image = cv2.imread(image_path)

    points = []
    for coordinate in coordinates:
        x, y = coordinate
        points.append([int(x), int(y)])

    points = np.array(points)
    points = points.reshape((-1, 1, 2))
    color = (255, 255, 0)
    thickness = 2
    isClosed = False
    image = cv2.polylines(image, [points], isClosed, color, thickness)

    # imageio.imwrite(image, cv2.resize(img, (512, 512)).astype(np.uint16))
