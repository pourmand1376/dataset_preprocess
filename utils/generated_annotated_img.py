#!/home/amir/miniconda3/envs/venv-ctscan/bin/python

"""
This file gets annotation and image folder  and draws annotation over images
"""
import json
from argparse import ArgumentParser
from pathlib import Path


def generate_annotated_img(image, annotation):
    pass


def main(args):
    images = Path(args.image_folder)

    if not images.is_dir:
        return ValueError("--image_folder should be a folder")

    annotations = Path(args.annotation).read_text()
    parsed_annotations = json.loads(annotations)

    for annotated_file in parsed_annotations:
        file_name, annotation = annotated_file


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--image_folder", "-f", required=True, dest="image_folder")
    parser.add_argument("--annotation", "-a", required=True, dest="annotation")
    args = parser.parse_args()

    main(args)
