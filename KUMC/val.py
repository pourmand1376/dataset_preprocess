"""This is to evaluate the results patient-wise!"""

from pathlib import Path

import typer

app = typer.Typer(name="Evaluate", add_completion=False)


def main(dataset_folder: str, prediction_labels_folder: str):
    """
    This function receives these arguments and produces patient-wise results.
    dataset_folder contains two folders images and labels.
    The program finds patient list via images folder and detects labels via labels folder.
    Then it compares that to prediction labels folder which is extracted via --save-txt
    parameter in yolo val.py file.
    """

    dataset_folder = Path(dataset_folder)
    prediction_labels_folder = Path(prediction_labels_folder)

    all_patients = set()
    images_folder = dataset_folder / "images"
    for image in images_folder.iterdir():
        all_patients.add(image.name.split("_")[0])
    print(all_patients)
    print(len(all_patients))


if __name__ == "__main__":
    app()
