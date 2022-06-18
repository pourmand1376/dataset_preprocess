"""
This file is the entry point in out program.
It gets a patient full sample or a directory containing full samples and converts them to yolo
"""

import re
from argparse import ArgumentParser
from pathlib import Path

from pydicom.filereader import dcmread

from utils import generate_dcm_image, parse_coordinates


def is_full_sample(folder: Path) -> bool:
    """
    This gets a folder and understands if it is a full sample (a patient with all of its data)
    """
    if not folder.is_dir():
        raise ValueError("passed argument is not a valid folder")

    for file in folder.iterdir():
        if (
            file.name == "AutoRun.exe"
            or file.name == "autorun.inf"
            or file.name == "PersianGulf_Help"
        ):
            return True

    return False


def find_all_numbers_folder(folder: Path):
    """
    This functions enumerates a folder and return a subfolder
    if the name of that subfolder consists of just numbers!
    This is for because inside DICOM folder we have this structure
    DICOM/20182124/13123/dcm_files
    """
    for item in folder.iterdir():
        match = re.match(r"^\d+$", item.name)
        if match:
            return folder / match[0]

    return None


def process_dcm_file(dcm_file: Path):
    pass


def find_dcm_files(folder: Path) -> list[Path]:
    """
    This method goes inside DICOM folder and finds all dcm files
    """
    dicomfolder = folder / "DICOM"

    if not dicomfolder.exists():
        raise ValueError("DICOM folder doesn't exists")

    inner_folder = find_all_numbers_folder(dicomfolder)
    dcm_folder = find_all_numbers_folder(inner_folder)

    dcm_files = []
    for file in dcm_folder.iterdir():
        if re.match(r"^\d+$", file.name):
            dcm_files.append(file)

    return dcm_files


def process_full_sample(folder: Path):
    """
    This function gets a verified full sample and processes it!
    """
    xml_annotation = folder / "CDViewer" / "studies.xml"
    if not xml_annotation.exists():
        raise ValueError("studies.xml file not found!")

    annotations = parse_coordinates.read_xml_annotations(xml_annotation, True)
    dcm_files = find_dcm_files(folder)

    if len(dcm_files) == 0:
        raise ValueError(f"No dcm files found in {folder}")

    png_dir = dcm_files[0].parent.parent / "png"
    png_dir.mkdir(exist_ok=True)
    for file in dcm_files:
        generate_dcm_image.generate_image_file(file, png_dir / f"{file.name}.png")


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
