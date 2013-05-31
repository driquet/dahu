# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides functions related to cache
"""

import os, shutil, sys
from dahu.core import album, image

def update_cache(root_path, cache_path, album_path, album_thumb_size, picture_sizes, verbose=False):
    """ Update the cache: generate all thumbnails (album and picture thumbnails) """

    inner_albums = album.get_album_dirs(root_path, album_path)
    album_pictures = album.get_album_pictures(root_path, album_path)


    # 1) Update the album thumbnail
    if verbose:
        sys.stdout.write('updating %s\n' % album_path)
    album.get_album_thumbnail(root_path, cache_path, album_path, album_thumb_size)


    # 2) Update pictures thumbnail
    for picture in album_pictures:
        if verbose:
            sys.stdout.write('updating %s\n' % os.path.join(album_path, picture))
        for size, is_thumb in picture_sizes:
            image.get_image(root_path, cache_path, album_path, picture, size, is_thumb)

    # 3) Propagate update
    for inner_album in inner_albums:
        update_cache(root_path, cache_path, os.path.join(album_path, inner_album), album_thumb_size, picture_sizes, verbose=verbose)


def clear_cache(cache_path, verbose=False):
    """ Clear the cache: remove all thumbnails """
    for elt in os.listdir(cache_path):
        elt_path = os.path.join(cache_path, elt)
        if os.path.isdir(elt_path):
            if verbose:
                sys.stdout.write('rm %s\n' % elt_path)
            shutil.rmtree(elt_path)
