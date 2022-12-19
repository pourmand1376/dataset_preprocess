## KUMC Dataset Semi-supervised 

Useful commands for this project

Replace all names of ".txt" files with ".jpg"
```bash
ls semi07-kvasir/labels/ | sed "s/.txt/.jpg/"
```

This one moves all ".jpg" who have label in "labels" folder to another folder
```bash
ls ../../semi07-kvasir/labels/ | sed "s/\.txt/\.jpg"/ | xargs cp -t ../../semi07-kvasir/images/
```