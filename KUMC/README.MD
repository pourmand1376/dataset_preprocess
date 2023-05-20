## To Convert the dataset to YOLO format
Add `dataset.yaml` in your kumc folder according to 
[this documentation](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data). 

It would be something like this:
```
path: path/to/kumc/folder
train: train2019
val: val2019
test: test2019
nc: 2
names: [hyperplastic, adenomatous]
```

You can also convert KUMC to YOLO format using this commands. This is not needed for YOLOv5. 

```bash
pip install -r requirements.txt
python kumc.py path/to/kumc/folder
python voc_to_yolo.py path/to/kumc/folder 'adenomatous,hyperplastic'
```
## KUMC Dataset Semi-supervised

Useful commands for this project

```bash
realpath dataset.yaml file #useful
```

Replace all names of ".txt" files with ".jpg"

```bash
ls semi07-kvasir/labels/ | sed "s/.txt/.jpg/"
```

This one moves all ".jpg" who have label in "labels" folder to another folder

```bash
ls ../../semi07-kvasir/labels/ | sed "s/\.txt/\.jpg"/ | xargs cp -t ../../semi07-kvasir/images/
```

This is for confi-thres=0.01 which we need images that do not have a label:

```bash
ls runs/detect/exp6/labels/ | sed "s/\.txt/\.jpg/" > exp6-labels.txt
```

Now we need to see which items exist in 1 but not in 2:

```bash
comm -23 all_images.txt ../semi001-kvasir/exp6-labels_sorted.txt > needed_to_copy.txt
```
