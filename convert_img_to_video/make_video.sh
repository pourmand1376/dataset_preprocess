# https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg
# make video from images
# first use fix_file_names
ffmpeg -framerate 30 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p out.mp4
