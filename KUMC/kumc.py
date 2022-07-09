"""
This file processes a KUMC dataset to make it suitable for YOLOv5
"""

import os
from pathlib import Path

import typer
from logger import logger

app = typer.Typer(name="KUMC Parser", add_completion=False)


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
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    for folder in input_folder.iterdir():
        if not folder.is_dir():
            continue

        _rename_files_append_folder(folder / "Annotation")
        _rename_files_append_folder(folder / "images")

        (folder / "Annotation").rename(output_folder / "Annotation")
        (folder / "Image").rename(output_folder / "images")


if __name__ == "__main__":
    app()
