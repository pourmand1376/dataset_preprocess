from pathlib import Path

import typer
import xmltodict

app = typer.Typer(name="Convert VOC to YOLO")


def _convert_box(xmin, xmax, ymin, ymax, width, height):
    x_mid = (xmin + xmax) / 2
    y_mid = (ymin + ymax) / 2
    width_bbox = xmax - xmin
    height_bbox = ymax - ymin

    x_mid = x_mid / width
    width_bbox = width_bbox / width

    y_mid = y_mid / height
    height_bbox = height_bbox / height

    return x_mid, y_mid, width_bbox, height_bbox


def _convert_voc_to_yolo(content: str, class_dict):
    content = content["annotation"]
    width = int(content["size"]["width"])
    height = int(content["size"]["height"])

    if isinstance(content["object"], dict):
        # make this a list if it only has one bbox
        content["object"] = [content["object"]]

    yolo_content = ""
    for object_ in content["object"]:
        class_index = class_dict[object_["name"]]
        bbox = object_["bndbox"]

        xmin = int(bbox["xmin"])
        xmax = int(bbox["xmax"])
        ymin = int(bbox["ymin"])
        ymax = int(bbox["ymax"])

        yolo_coordinates = _convert_box(
            xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, width=width, height=height
        )
        bbox_info = f"{class_index} {yolo_coordinates[0]} {yolo_coordinates[1]} {yolo_coordinates[2]} {yolo_coordinates[3]}"

        if len(yolo_content) == 0:
            yolo_content = bbox_info
        else:
            yolo_content = yolo_content + "\n" + bbox_info

    return yolo_content


@app.command()
def main(
    dataset_dir: str = typer.Argument(
        ..., help="the directory that contains annotations"
    ),
    classes: str = typer.Argument(..., help="Class names splited by comma"),
):
    """
    You input your dataset directory here
    and the program will try to find all xml files within the folder recursively
    and convert them to yolo format.

    This code does not change file name to something odd.
    Just xml is converted into txt.
    """
    dataset_dir = Path(dataset_dir)
    classes_dict = {}

    for index, item in enumerate(classes.split(",")):
        classes_dict[item] = index

    for file in dataset_dir.glob("**/*.xml"):
        text = file.read_text()
        content = xmltodict.parse(text)
        yolo_content = _convert_voc_to_yolo(content, classes_dict)

        sibling_parent = file.parent.parent / "labels"
        sibling_parent.mkdir(exist_ok=True, parents=True)
        output_file = sibling_parent / file.name.replace("xml", "txt")
        output_file.write_text(yolo_content)


if __name__ == "__main__":
    app()
