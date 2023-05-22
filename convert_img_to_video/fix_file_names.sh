# https://stackoverflow.com/questions/3211595/renaming-files-in-a-folder-to-sequential-numbers 
# this is needed since we might have images like 1.jpg and 10.jpg
num=0; for i in *; do mv "$i" "$(printf '%04d' $num).${i#*.}"; ((num++)); done
