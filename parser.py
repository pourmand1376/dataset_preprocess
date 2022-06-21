"""
This file is the entry point in out program.
It gets a patient full sample or a directory containing full samples
and converts them to yolo
"""

import re
from multiprocessing import Pool
from pathlib import Path

import typer

from logger import logger
from utils import annotate, coordinate, dicom_image
from utils.utility import find_all_numbers_folder, move_folder

app = typer.Typer(name="Parser DICOM", add_completion=False)


def is_full_sample(folder: Path) -> bool:
    """
    This gets a folder and understands if it is a full sample
    (a patient with all of its data)
    """
    if not folder.is_dir():
        raise ValueError("passed argument is not a valid folder")

    for file in folder.iterdir():
        if (
            file.name == "AutoRun.exe"
            or file.name == "autorun.inf"
            or file.name == "PersianGulf_Help"
            or file.name == "WebViewer"
            or file.name == "CDViewer"
        ):
            return True

    return False


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
    logger.info(f"About to Process Folder {folder}")
    xml_annotation = folder / "CDViewer" / "studies.xml"
    if not xml_annotation.exists():
        raise ValueError("studies.xml file not found!")

    annotations = coordinate.read_xml_annotations(xml_annotation, True)
    logger.info("annotations are parsed to json")
    dcm_files = find_dcm_files(folder)

    if len(dcm_files) == 0:
        raise ValueError(f"No dcm files found in {folder}")

    png_dir = dcm_files[0].parent.parent / "png"
    png_dir.mkdir(exist_ok=True)
    for file in dcm_files:
        file_name = "_".join(str(file).split("/")[-5:])
        png_file = png_dir / f"{file_name}.png"
        dicom_image.generate_image_file(file, png_file)

    yolo_dir = annotate.process_needed_files(png_dir, annotations)

    logger.info(f"PNG Dir {png_dir}")
    logger.info(f"YOLO Dir {yolo_dir}")

    return png_dir, yolo_dir


def post_process_sample(png_dir: Path, yolo_dir: Path, output_folder: Path):
    logger.info("Post Processing")
    if not output_folder.exists():
        logger.info(f"creating folder {output_folder}")
        output_folder.mkdir(exist_ok=True)

    logger.info(f"moving {png_dir} to {output_folder}")

    images_dir = output_folder / "images"
    if not images_dir.exists():
        images_dir.mkdir(exist_ok=True)

    move_folder(png_dir, images_dir)
    png_dir.rmdir()

    if yolo_dir is None:
        return

    logger.info(f"moving {yolo_dir} to {output_folder}")

    labels_dir = output_folder / "labels"
    if not labels_dir.exists():
        labels_dir.mkdir(exist_ok=True)
    move_folder(yolo_dir, output_folder / "labels")
    yolo_dir.rmdir()


def check_process_sample(input_folder: Path, output_folder):
    try:
        if not input_folder.is_dir():
            logger.warning(
                f"{input_folder} is not a valid folder to process as full sample"
            )
            return None

        if not is_full_sample(input_folder):
            logger.warning(f"{input_folder} is not a valid full sample!")

            # this is odd. sometimes data is in inner folder, we should check one level more!
            # but this happens only if the inner folder has 1 subfolder
            # This happens only in Normal folder
            if len(list(input_folder.iterdir())) == 1:
                first_subfolder = next(input_folder.iterdir())
                return check_process_sample(first_subfolder, output_folder)

            return None

        png_dir, yolo_dir = process_full_sample(input_folder)
        logger.info(f"full sample processed: {input_folder}")
        if output_folder:
            post_process_sample(png_dir, yolo_dir, output_folder)
            logger.info(
                f"post process sample done from: {input_folder} to:{output_folder}"
            )

    except BaseException:
        logger.error("Error Happened!", exc_info=True)


@app.command()
def main(input_folder: str, output_folder: str = None, cores: int = 1):
    """
    There are two possible ways inputpath can be interpreted

    First: It can be interpreted as a single (full) sample.

    Second: It will be interpreted as a folder containing multiple samples
    In this case, we will process each subfolder accordingly.
    """
    input_folder = Path(input_folder)
    if output_folder:
        output_folder = Path(output_folder)

    if is_full_sample(input_folder):
        logger.info("Processing Just One sample")
        check_process_sample(input_folder, output_folder)
    # if it is not a full sample, it is a list of full samples!
    else:
        logger.info("Processing Batch of samples")

        pool = Pool(processes=cores)
        logger.info(f"using {cores} cores!")
        counts = pool.starmap(
            check_process_sample,
            [(folder, output_folder) for folder in input_folder.iterdir()],
        )
        logger.info(f"Found {counts} spots!")
        logger.info("Processing Successfully finished")


if __name__ == "__main__":
    app()
