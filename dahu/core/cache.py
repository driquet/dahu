# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides functions related to cache
"""

import os, shutil
from dahu.core import album, image

def update_cache(root_path, cache_path, album_path, album_thumb_size, picture_sizes):
    """ Update the cache: generate all thumbnails (album and picture thumbnails) """
    inner_albums = album.get_album_dirs(root_path, album_path)
    album_pictures = album.get_album_pictures(root_path, album_path)

    print album_path

    # 1) Update the album thumbnail
    album.get_album_thumbnail(root_path, cache_path, album_path, album_thumb_size)

    print "%s/%s" % (album_path, 'thumb.jpg')

    # 2) Update pictures thumbnail
    for picture in album_pictures:
        for size, is_thumb in picture_sizes:
            image.get_image(root_path, cache_path, album_path, picture, size, is_thumb)
            print "%s/%s/%d" % (album_path, picture, size)

    # 3) Propagate update
    for inner_album in inner_albums:
        update_cache(root_path, cache_path, os.path.join(album_path, inner_album), album_thumb_size, picture_sizes)


def clear_cache(cache_path):
    """ Clear the cache: remove all thumbnails """
    for elt in os.listdir(cache_path):
        elt_path = os.path.join(cache_path, elt)
        if os.path.isdir(elt_path):
            print elt_path
            shutil.rmtree(elt_path)
