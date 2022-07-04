import os
import re
import shutil
from pathlib import Path

from logger import logger


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
            logger.info(f"found folder {folder/match[0]}")
            return folder / match[0]

    return None


def move_folder(from_dir, to_dir):

    from_dir = str(from_dir)
    to_dir = str(to_dir)

    file_names = os.listdir(from_dir)

    for file_name in file_names:
        shutil.move(os.path.join(from_dir, file_name), to_dir)
