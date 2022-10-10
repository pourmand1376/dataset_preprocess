"""This is to evaluate the results patient-wise!"""

from pathlib import Path

import typer

app = typer.Typer(name="Evaluate", add_completion=False)


@app.command()
def main(dataset_folder: str, prediction_labels_folder: str, min_count: int = 2):
    """
    This function receives these arguments and produces patient-wise results.
    dataset_folder contains two folders images and labels.
    The program finds patient list via images folder and detects labels via labels folder.
    Then it compares that to prediction labels folder which is extracted via --save-txt
    parameter in yolo val.py file.
    Min_count: minimum number of images to make a patient positive.
    """

    dataset_folder = Path(dataset_folder)
    prediction_labels_folder = Path(prediction_labels_folder)

    all_patients = set()
    images_folder = dataset_folder / "images"
    for image in images_folder.iterdir():
        all_patients.add(image.name.split("_")[0])

    real_positive_patients = set()
    real_labels_folder = dataset_folder / "labels"

    for label in real_labels_folder.iterdir():
        real_positive_patients.add(label.name.split("_")[0])

    pred_positive_patients_ = dict()
    pred_positive_patients = set()

    for label in prediction_labels_folder.iterdir():
        category = label.name.split("_")[0]
        if category in pred_positive_patients_:
            pred_positive_patients_[category] = pred_positive_patients_[category] + 1
        else:
            pred_positive_patients_[category] = 1

        if pred_positive_patients_[category] >= min_count:
            pred_positive_patients.add(category)

    negatives = all_patients.difference(real_positive_patients)
    neg_pred = all_patients.difference(pred_positive_patients)

    tp = len(real_positive_patients.intersection(pred_positive_patients))
    fp = len(pred_positive_patients.difference(real_positive_patients))
    fn = len(real_positive_patients.difference(pred_positive_patients))
    tn = len(negatives.intersection(neg_pred))

    print(f"TP: {tp}, FP: {fp}, FN: {fn}, TN: {tn}")

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print(f"Precision: {precision}, recall: {recall}")


if __name__ == "__main__":
    app()
