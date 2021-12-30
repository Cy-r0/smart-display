#!/usr/bin/env python3

"""Take a directory with photos and rename consecutive pairs
based on a user-given list of names.
"""

__author__ = 'Ciro Cursio'

import os
import shutil
import sys

from natsort import os_sorted


def rename_photos(in_dir, out_dir, names_list):

    files_list = [f for f in os_sorted(os.listdir(in_dir))]
    print(files_list)
    assert len(names_list) == len(files_list) // 2

    if not os.path.isdir(out_dir):
        print(f'{out_dir} does not exist, creating...')
        os.makedirs(out_dir)

    for i, file in enumerate(files_list):
        in_path = os.path.join(in_dir, file)

        # Put together new filename
        name = names_list[i//2]
        antepost = 'ante' if i % 2 == 0 else 'post'
        ext = os.path.splitext(file)[1]

        new_file = name + '_' + antepost + ext
        out_path = os.path.join(out_dir, new_file)
        shutil.copy(in_path, out_path)
        print(f'Copied {in_path} to {out_path}')


if __name__ == '__main__':
    rename_photos(sys.argv[1], sys.argv[2], sys.argv[3:])
