#!/usr/bin/env python3

#
# This is intended to be triggered when an sdcard is inserted into a Mac. It looks for a Volume with a DCIM directory
# and imports new files into a photo library hierarchy.
# I used AppleScript to trigger this when any new filesystem is mounted.
#

import datetime
import os
import shutil
from os.path import exists

# Path to photo library.
image_library_path = os.environ.get('HOME') + '/Pictures/photo-library'

# Look for a Volume that looks like a mounted camera sdcard.
def find_sdcard_root():
    for file in os.listdir('/Volumes'):
        path = f'/Volumes/{file}/DCIM'
        if os.path.isdir(path):
            return path
    return None


def get_file_info(filename, directory):
    file_info = {}
    path = os.path.join(directory, filename)
    stat = os.stat(path)
    file_size = stat.st_size
    mtime = stat.st_mtime
    ts = datetime.datetime.fromtimestamp(mtime)
    file_info['filename'] = filename
    file_info['src_dir'] = directory
    file_info['src_path'] = path
    file_info['timestamp'] = ts
    file_info['file_size'] = file_size
    file_info['dst_dir'] = get_dst_dir(file_info)
    file_info['dst_path'] = os.path.join(file_info['dst_dir'], filename)

    return file_info


def get_dst_dir(file_info):
    dst_path = image_library_path + file_info['timestamp'].strftime("/%Y/%m/%d/")
    return dst_path


def get_copy_filename(file_info):
    index = 1
    filename, extension = os.path.splitext(file_info['dst_path'])
    print(filename, extension)
    while index < 10:
        dst_path = filename + '_' + str(index) + extension
        if not exists(dst_path):
            return dst_path
    return None


def copy_file(file_info):
    if not exists(file_info['dst_path']):
        print(f"copying {file_info['src_path']} to {file_info['dst_path']}")
        os.makedirs(file_info['dst_dir'], exist_ok=True)
        shutil.copy2(file_info['src_path'], file_info['dst_path'])
    else:
        # File exists: skip overwrite if it's identical, make a copy if not
        stat = os.stat(file_info['dst_path'])
        dst_file_size = stat.st_size
        if dst_file_size == file_info['file_size']:
            print(f"skipping overwrite of {file_info['dst_path']}")
        else:
            copy_filename = get_copy_filename(file_info)
            if copy_filename is None:
                print(f"Too many copies of {file_info['dst_path']}, bailing out")
            else:
                os.makedirs(file_info['dst_dir'], exist_ok=True)
                shutil.copy2(file_info['src_path'], copy_filename)


def process_file(filename, directory):
    file_info = get_file_info(filename, directory)
    copy_file(file_info)

# Start of the actual script.
sdcard_root = find_sdcard_root()
if sdcard_root is None:
    print('no sdcard found')
    exit(1)
print(f' Found sdcard {sdcard_root}')

for subdir, d_names, f_names in os.walk(sdcard_root):
    for f in f_names:
        filename = str(f).upper()
        if filename.endswith(".JPG") or filename.endswith(".NEF"):
            path_on_card = f'{subdir}/{filename}'
            process_file(filename, subdir)
            print(path_on_card)
