"""
This file processes a KUMC dataset to make it suitable for YOLOv5
"""

import os
from pathlib import Path

import sh
import typer
from logger import logger

app = typer.Typer(name="KUMC Parser", add_completion=False)


def _move_all_subfolder_files_to_main_folder(folder_path: Path):
    """
    This function will move all files in all subdirectories to the folder_path dir.
    folder_path/
        1/
            1.jpg
            2.jpg
    outputs:
    folder_path/
        1.jpg
        2.jpg
    """
    if not folder_path.is_dir():
        return

    for subfolder in folder_path.iterdir():
        for file in subfolder.glob("*/*"):
            file.rename(subfolder / file.name)


def _rename_files_append_folder(folder_path: Path):
    """
    this method receives a folder like this
    test/
        1.xml
        2.xml
        3.xml
    and outputs this
    test/
        test_1.xml
        test_2.xml
        test_3.xml
    """
    folder_path = str(folder_path)
    for dirpath, _, files in os.walk(folder_path):
        for f in files:
            from_ = os.path.join(dirpath, f)
            to = os.path.join(dirpath, os.path.split(dirpath)[-1] + "_" + f)

            logger.info(f"renaming from {from_} to {to}")
            os.rename(from_, to)


@app.command()
def main(input_folder: str, output_folder):
    """
    this one receives a path which has following structure in it
    input_folder(KUMC)/
        train2019/
            Annotation/
            Image/
        test2019/
        val2019/
    """
    try:
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)

        for folder in input_folder.iterdir():
            if not folder.is_dir():
                continue

            from_annotation_folder = folder / "Annotation"
            from_image_folder = folder / "Image"

            logger.info(f"Start preprocess folder {from_annotation_folder}")
            _rename_files_append_folder(from_annotation_folder)
            logger.info(f"Start preprocess folder {from_image_folder}")
            _rename_files_append_folder(from_image_folder)

            to_annotation_folder = output_folder / folder.name / "Annotation"
            to_images_folder = output_folder / folder.name / "images"

            logger.info(
                f"creating folder {to_annotation_folder} and {to_images_folder}"
            )
            to_annotation_folder.mkdir(exist_ok=True, parents=True)
            to_images_folder.mkdir(exist_ok=True, parents=True)

            logger.info(f"moving {from_annotation_folder} to {to_annotation_folder}")
            from_annotation_folder.rename(to_annotation_folder)
            logger.info(f"moving {from_image_folder} to {to_images_folder}")
            from_image_folder.rename(to_images_folder)

            _move_all_subfolder_files_to_main_folder(to_images_folder)
            _move_all_subfolder_files_to_main_folder(to_annotation_folder)

    except Exception:
        logger.error(exc_info=True)


if __name__ == "__main__":
    app()
