# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides functions related to albums
"""

import os, re, random
from PIL import Image, ImageOps

picture_re = re.compile(r'.*\.jpg$', re.IGNORECASE)


def is_valid_path(root_path, local_path):
    """ Returns whether or not a path is valid """
    return os.path.exists(os.path.join(root_path, local_path))


def get_album_dirs(root_path, album_path):
    """ This method returns the inner albums related to an album """
    albums = []
    album_path = os.path.join(root_path, album_path)

    for elt in os.listdir(album_path):
        elt_path = os.path.join(root_path, album_path, elt)
        if os.path.isdir(elt_path):
            albums.append(elt)

    return albums


def get_album_pictures(root_path, album):
    """ This method returns the pictures related to an album """
    pictures = []
    album_path = os.path.join(root_path, album)

    for elt in os.listdir(album_path):
        elt_path = os.path.join(root_path, album_path, elt)
        if os.path.isfile(elt_path):
            match = re.match(picture_re, elt)
            if match:
                pictures.append(elt)

    return pictures

def get_album_number_pictures(root_path, album_path):
    """ Return the number of pictures in an album """
    return len(get_album_pictures(root_path, album_path))


def get_album_total_number_pictures(root_path, album_path):
    """ Return the total number (recursively) of an album """
    number = get_album_number_pictures(root_path, album_path)

    for inner_album in get_album_dirs(root_path, album_path):
        number += get_album_total_number_pictures(root_path, os.path.join(album_path, inner_album))

    return number


def create_album_thumbnail(root_path, cache_path, album_path, album_picture, size, thumb_name='thumb.jpg'):
    thumbnail_dir = os.path.join(cache_path, album_path)

    # Creating the cache directory if it does not exist
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    # Creating the thumbnail
    image = Image.open(os.path.join(root_path, album_path, album_picture))
    image = ImageOps.fit(image, (size, size), Image.ANTIALIAS)
    image.save(os.path.join(thumbnail_dir, thumb_name))


def get_album_thumbnail(root_path, cache_path, album_path, size):
    thumbnail_name = 'thumb.jpg'
    thumbnail_dir = os.path.join(cache_path, album_path)

    # Create the thumbnail if it does not exist
    if not os.path.exists(os.path.join(thumbnail_dir, thumbnail_name)):
        # Select a random picture form the album
        pictures = get_album_pictures(root_path, album_path)
        if len(pictures):
            original_picture = random.choice(pictures)
            create_album_thumbnail(root_path, cache_path, album_path, original_picture, size, thumbnail_name)

        else:
            inner_albums = get_album_dirs(root_path, album_path)
            for inner_album in inner_albums:
                inner_thumb = get_album_thumbnail(root_path, cache_path, os.path.join(album_path, inner_album), size)
                if inner_thumb:
                    return inner_thumb
            # No pictures in this album
            # Several solutions :
            #   - pick a picture from an inner albums
            #   - default image for empty albums
            return None

    return (thumbnail_dir, thumbnail_name)
