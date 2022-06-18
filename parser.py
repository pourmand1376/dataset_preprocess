"""
This file is the entry point in out program.
It gets a patient full sample or a directory containing full samples and converts them to yolo
"""

from argparse import ArgumentParser
from pathlib import Path


def is_full_sample(folder: Path) -> bool:
    """
    This gets a folder and understands if it is a full sample (a patient with all of its data)
    """
    if not folder.is_dir():
        return ValueError("passed argument is not a valid folder")

    for file in folder.iterdir():
        if (
            file.name == "AutoRun.exe"
            or file.name == "autorun.inf"
            or file.name == "PersianGulf_Help"
        ):
            return True

    return False


def process_full_sample(folder: Path):
    """
    This function gets a verified full sample and processes it!
    """
    xml_annotation = folder / "CDViewer" / "studies.xml"
    if not xml_annotation.exists():
        return ValueError("studies.xml file not found!")

    xml_annotation.read_text()


def main(args):
    input_path = Path(args.folder)
    if is_full_sample(input_path):
        process_full_sample(input_path)

    # if it is not a full sample, it is a list of full samples!
    else:
        for file in input_path.iterdir():
            if file.is_dir():
                if is_full_sample(file):
                    process_full_sample(file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--folder", required=True, dest="folder")
    args = parser.parse_args()

    main(args)
