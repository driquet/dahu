#!/usr/bin/env python
'''
File: autorotate.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: This script provides an auto-rotate feature of pictures based on Exif data
'''

import os, re, argparse
from PIL import Image

picture_re = re.compile(r'.*\.jpg$', re.IGNORECASE)

def autorotate(path, filename):
    """ This function autorotates a picture """
    image = Image.open(os.path.join(path, filename))
    exif = image._getexif()
    if not exif:
        return False

    orientation_key = 274 # cf ExifTags
    if orientation_key in exif:
        orientation = exif[orientation_key]

        rotate_values = {
            3: 180,
            6: 270,
            8: 90
        }

        if orientation in rotate_values:
            # Rotate and save the picture
            image = image.rotate(rotate_values[orientation])
            image.save(os.path.join(path, filename), quality=100)

            print "autoroate"
            return True

    return False


def process_directory(path, recursive=False):
    """ This function processes all elements from a directory """
    for elt in os.listdir(path):
        elt_path = os.path.join(path, elt)
        if os.path.isdir(elt_path):
            process_directory(os.path.join(path, elt), recursive)

        elif os.path.isfile(elt_path):
            match = re.match(picture_re, elt_path)
            if match:
                if autorotate(path, elt_path):
                    print 'autorotate: %s/%s' % (path, elt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='+')
    parser.add_argument('--recursive', '-r', action='store_true')
    args = parser.parse_args()

    for directory in args.directory:
        process_directory(directory, args.recursive)
