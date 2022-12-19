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