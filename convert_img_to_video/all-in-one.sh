#!/bin/bash
for i in {1..24}
do
   cd /home/user01/pourmand/yolov5/
   python detect.py --source "/mnt/new_drive/pourmand/KUMC-Harvard/PolypsSet/test2019/Image/$i" \
    --weights runs/train/exp8/weights/best.pt
done

for j in {25..48}
do
    cd "/home/user01/pourmand/yolov5/runs/detect/exp$j"
    num=0; for i in *; do mv "$i" "$(printf '%04d' $num).${i#*.}"; ((num++)); done
    ffmpeg -framerate 30 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p "exp$j.mp4"
done

mv **/*.mp4 .