import argparse
import os
import hashlib

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

parser = argparse.ArgumentParser(description='Find duplicate photos')
parser.add_argument('--srcdir', dest='srcdir',
                    help='source directory containing photos')
args = parser.parse_args()
print(args.srcdir)

signatures = dict()
file_count = 0
duplicate_count = 0

with open(os.path.join(args.srcdir, 'delete_duplicates.sh'), 'w') as dups_file:
    for subdir, d_names, f_names in os.walk(args.srcdir):
        for f in f_names:
            if str(f).endswith(".sh"):
                continue
            # print(f"file = {f}")
            # print(f"subdir = {subdir}")
            p = os.path.join(subdir, f)
            size = os.stat(p).st_size
            # print(f"file = {p}")
            md5 = md5sum(p)
            # print(f"md5 = {md5}")
            key = str(size) + '-' + md5
            if key in signatures:
                print(f"{key} already found for file {signatures[key]}")
                duplicate_count += 1
                print(f"rm {p}", file=dups_file)
                if duplicate_count % 10 == 0:
                    print(f"found {duplicate_count} duplicates")
            else:
                signatures[key] = p
            file_count += 1
            if file_count % 100 == 0:
                print(f"processed {file_count} files")
print(f"found {duplicate_count} duplicates in {file_count} files")