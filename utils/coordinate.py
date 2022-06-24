#!/home/amir/miniconda3/envs/venv-ctscan/bin/python
"""
This file parses studies.xml file.
You can refer here for more information:
    https://github.com/pydicom/pydicom/discussions/1653
"""

import json
import re
from pathlib import Path

import typer
from xmltodict import parse

from logger import logger

app = typer.Typer(name="Parse XML file", add_completion=False)


def _parse_annotations(sample: dict):

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

    if annotation.count(".") != len(coordinates):
        logger.error(f"We couldn't match all coordinates {file_name}")

    return (file_name, coordinates)


def read_xml_annotations(read_file: Path, json_output: bool = True):
    logger.info(f"About to read {read_file}")
    text = read_file.read_text()
    parsed_data = parse(text)
    series = parsed_data["studies"]["study"]["series"]

    annotations = []

    for item in series:
        instance = item["instance"]

        if type(instance) is dict:
            annotation = _parse_annotations(instance)
            if annotation is None:
                continue
            annotations.append(annotation)

        elif type(instance) is list:
            for sample in instance:
                annotation = _parse_annotations(sample)
                if annotation is None:
                    continue
                annotations.append(annotation)

    json_file = read_file.parent / "annotations.json"
    if json_output:
        Path(json_file).write_text(json.dumps(annotations))
        logger.info(f"Just wrote {json_file}")

    return annotations


def main(xml_file: str):
    read_xml_annotations(Path(xml_file), True)


if __name__ == "__main__":
    app()
