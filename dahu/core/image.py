# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides functions related to image
"""

from PIL import Image, ImageOps
import os


def get_image(root_path, cache_path, album, filename, size=None, thumbnail=False):
    if size == None or size == 'full':
        image_dir = os.path.join(root_path, album)

    else:
        cache_dir = 'thumbnail' if thumbnail else str(int(size))
        image_dir = os.path.join(cache_path, album, cache_dir)

        # Creating the cache directory if it does not exist
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Creating the cache image if it does not exist
        if not os.path.exists(os.path.join(image_dir, filename)):
            create_image(root_path, cache_path, album, filename, int(size), thumbnail)

    return (image_dir, filename)


def create_image(root_path, cache_path, album, filename, size, thumbnail=False):
    cache_dir = 'thumbnail' if thumbnail else str(int(size))
    image_dir = os.path.join(cache_path, album, cache_dir)
    orig_dir = os.path.join(root_path, album)

    # Creating the cache directory if it does not exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image = Image.open(os.path.join(orig_dir, filename))
    if thumbnail:
        image = ImageOps.fit(image, (size, size), Image.ANTIALIAS)
    else:
        image.thumbnail((int(size), int(size)), Image.ANTIALIAS)

    image.save(os.path.join(image_dir, filename))
