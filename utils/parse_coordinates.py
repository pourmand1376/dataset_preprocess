#!/home/amir/miniconda3/envs/venv-ctscan/bin/python
"""
This file parses studies.xml file.
You can refer here for more information:
    https://github.com/pydicom/pydicom/discussions/1653
"""

import json
import re
from argparse import ArgumentParser
from pathlib import Path

from xmltodict import parse


def read_annotations(sample: dict):

    if "annotation" not in sample.keys():
        return None

    file_name = sample["file_name"]
    annotation = sample["annotation"]

    if not annotation or annotation is None:
        return None

    values = re.findall(r"\d{3}\.\d{6}", annotation)

    coordinates = []
    while len(values) > 0:
        x = values.pop(0)
        y = values.pop(0)
        coordinates.append({"x": x, "y": y})

    return (file_name, coordinates)


def read_xml_annotations(read_file: Path, json_output: bool = True):
    text = read_file.read_text()
    parsed_data = parse(text)
    series = parsed_data["studies"]["study"]["series"]

    annotations = []

    for item in series:
        instance = item["instance"]

        if type(instance) is dict:
            annotation = read_annotations(instance)
            if annotation is None:
                continue
            annotations.append(annotation)

        elif type(instance) is list:
            for sample in instance:
                annotation = read_annotations(sample)
                if annotation is None:
                    continue
                annotations.append(annotation)
    json_file = read_file.parent / "annotations.json"
    if json_output:
        Path(json_file).write_text(json.dumps(annotations))


def main(args):
    read_xml_annotations(Path(args.read_file), True)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        dest="read_file",
        required=True,
    )
    args = parser.parse_args()

    main(args)
