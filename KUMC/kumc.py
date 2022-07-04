"""
This file processes a KUMC dataset to make it suitable for YOLOv5
"""

from pathlib import Path

import typer

from ..logger import logger

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
    if not folder_path.is_dir():
        logger.warning("given path is not folder")
        return

    for file in folder_path.iterdir():
        if file.is_dir():
            loggger.warning(f"file {file} is ignored")
            continue

        new_name = f"{file.parent.name}_{file.name}"
        file.rename(new_name)
        logger.info(f"file {file.name} renamed to {new_name}")


@app.command()
def main(input_folder: str):
    """
    this one receives a path which has following structure in it
    input_folder(KUMC)/
        train2019/
        test2019/
        val2019/
    """
    input_folder = Path(input_folder)
    for folder in input_folder.iterdir():
        if not folder.is_dir():
            continue

        _rename_files_append_folder(folder)


if __name__ == "__main__":
    app()
