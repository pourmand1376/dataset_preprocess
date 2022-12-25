# DICOM - Aneurysm

This project receives a folder containing patients who have done a CT-Scan and extracts images from all subfolders. The code is written to be compatible for specific data we have used. 

`DICOM` files are stored normally but annotations are stored in a weird format which I have described [here](https://github.com/pydicom/pydicom/discussions/1653).

You should run `parser.py` file to convert dataset to correct format and that's it!

It is also good to know that Recall, Precision and MAP is generated via `conf=0.001` but Patient-wise result is generated via `conf=0.3`. This is important since mAP would be wrong in `conf>0.01`. 