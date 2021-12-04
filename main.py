import argparse
import os
from os.path import exists
import re
import shutil

parser = argparse.ArgumentParser(description='Copy photos to a global photo library')
parser.add_argument('--srcdir', dest='srcdir',
                    help='source directory containing photos')
parser.add_argument('--dstdir', dest='dstdir',
                    help='destination directory')
args = parser.parse_args()
print(args.srcdir)
print(args.dstdir)

for root, d_names, f_names in os.walk(args.srcdir):
    for f in f_names:
        print("file = ", f)
        print("root = ", root)
        src = os.path.join(root, f)
        m = re.search('.+Masters/(.+?)$', root)
        subdir = root
        if m:
            subdir = m.group(1)
            subdir = re.sub(r"\d{8}-\d{6}$", "", subdir)
        # print(subdir)
        d = os.path.join(args.dstdir, subdir)
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, f)
        # print("dest = ", dst)
        print(f"copy {src} to {dst}")
        if not exists(dst):
            shutil.copy2(src, dst)
        else:
            print(f"skipping overwrite of {dst}")

