import argparse
import datetime
import os
from exif import Image
from datetime import datetime

#
# A utility script that looks in a given directory for images in a yyyy/mm/dd directory hierarchy.
# The EXIF data for each image is examined for the
# Any duplicate files are recorded as 'rm' commands in a output script: {srcdir}/delete_duplicates.sh
# After this program completes, run move_misplaced_photos.sh to move the misplaced images
# to the correct location in the photo-library.
#
image_library_path = os.environ.get('HOME') + '/Pictures/photo-library'

parser = argparse.ArgumentParser(description='Find duplicate photos')
parser.add_argument('--srcdir', dest='srcdir',
                    help='source directory containing photos')
args = parser.parse_args()
print(args.srcdir)

file_count = 0
duplicate_count = 0

def get_exif_dst_path(filename, dir):
    my_image = Image(os.path.join(dir, filename))
    datetime_original = str(my_image.datetime_original)
    dt = datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")
    src_path = os.path.join(dir, filename)
    dst_dir = image_library_path + "/" + dt.strftime("%Y/%m/%d/")
    dst_path = dst_dir + filename
    if src_path != dst_path:
        print(f"{src_path} != {dst_path}")
        print(f"mkdir -p  {dst_dir}", file=dups_file)
        print(f"mv {src_path} {dst_path}", file=dups_file)
    else:
        print(f"{src_path} is correct")


with open(os.path.join(args.srcdir, 'move_misplaced_photos.sh'), 'w') as dups_file:
    for subdir, d_names, f_names in os.walk(args.srcdir):
        for f in f_names:
            if not str(f).lower().endswith(".jpg"):
                continue
            get_exif_dst_path(f, subdir)