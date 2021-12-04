import argparse
import datetime
import os
from exif import Image
from datetime import datetime
import logging
from os.path import exists

parser = argparse.ArgumentParser(description='Move photos to hierarchy')
parser.add_argument('--srcdir', dest='srcdir', help='source directory containing photos')
parser.add_argument('--dstdir', dest='dstdir', help='destination directory')
args = parser.parse_args()
print(args.srcdir)

file_count = 0
duplicate_count = 0

def get_file_info(filename, directory):
    file_info = {}
    path = os.path.join(directory, filename)
    stat = os.stat(path)
    file_size = stat.st_size
    mtime = stat.st_mtime
    ts = datetime.fromtimestamp(mtime)
    file_info['filename'] = filename
    file_info['src_dir'] = directory
    file_info['src_path'] = path
    file_info['timestamp'] = ts
    file_info['file_size'] = file_size
    file_info['dst_dir'] = get_dst_dir(file_info)
    file_info['dst_path'] = os.path.join(file_info['dst_dir'], filename)
    return file_info


def get_dst_dir(file_info):
    dst_path = args.dstdir + file_info['timestamp'].strftime("/%Y/%m/%d/")
    return dst_path


def add_mv_entry(file_info):
    try:
        if not exists(file_info['dst_path']):
            print(f"copying {file_info['src_path']} to {file_info['dst_path']}")
            print(f"mkdir -p  {file_info['dst_dir']}", file=dups_file)
            print(f"cp {file_info['src_path']} {file_info['dst_path']}", file=dups_file)
        else:
            # File exists: skip overwrite if it's identical, make a copy if not
            # stat = os.stat(file_info['dst_path'])
            # dst_file_size = stat.st_size
            # if dst_file_size == file_info['file_size']:
            print(f"skipping overwrite of {file_info['dst_path']}")
            # else:
            #     src_path = os.path.join(dir, filename).replace(" ", "\\ ")
            #     my_image = Image(os.path.join(dir, filename))
            #     datetime_original = str(my_image.datetime_original)
            #     dt = datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")
            #     dst_dir = args.dstdir + "/" + dt.strftime("%Y/%m/%d/")
            #     dst_path = dst_dir + filename
            #     print(f"mkdir -p  {dst_dir}", file=dups_file)
            #     print(f"cp {src_path} {dst_path}", file=dups_file)
    except KeyError:
        logging.error(f"Error getting EXIF from {file_info['src_path']}")


with open(os.path.join(args.srcdir, '/Users/swhite/copy_photos.sh'), 'w') as dups_file:
    for subdir, d_names, f_names in os.walk(args.srcdir):
        for f in f_names:
            if not str(f).lower().endswith(".jpg"):
                continue
            file_info = get_file_info(f, subdir)
            add_mv_entry(file_info)