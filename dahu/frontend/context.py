'''
File: context.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Create a context for web requests
'''

import os
from flask import url_for, current_app
from dahu.core import album


def split_path(s):
    """
    This function split properly a path
    For example: 'A/B/C/D' will be splitted as ['A', 'B', 'C', 'D']
    """
    head, tail = os.path.split(s)
    if head == '':
        return tail,
    return split_path(head) + (tail,)


def get_linked_path(path):
    """
    Return the path (and corresponding links) of albums to reach the current album
    It returns a list as follow: [(album, link), ..., (album, link)]
    """
    splitted_path = split_path(path)
    full_path = [('Home', url_for('.show_album', album_path=''))]
    current_path = ''

    for p in splitted_path:
        if p:
            current_path = os.path.join(current_path, p)
            full_path.append((p, url_for('.show_album', album_path=current_path)))

    return full_path


def generate_album_context(current_album):
    """ Generate data context (pictures, links, and so on) for the current album """
    context = {}

    # Related data about the album
    context['name'] = current_album
    context['pictures'] = album.get_album_pictures(current_app.config['ALBUMS_PATH'], current_album)

    # Generate inner albums related data
    context['inner_albums'] = []
    for a in album.get_album_dirs(current_app.config['ALBUMS_PATH'], current_album):
        context['inner_albums'].append({
            'name' : a,
            'link' : url_for('.show_album', album_path=os.path.join(current_album, a)),
            'path' : os.path.join(current_album, a),
            'nb_pictures' : album.get_album_number_pictures(current_app.config['ALBUMS_PATH'], os.path.join(current_album, a)),
            'total_nb_pictures' : album.get_album_total_number_pictures(current_app.config['ALBUMS_PATH'],  os.path.join(current_album, a)),
        })

    # Generate the path of the current album
    context['linked_path'] = get_linked_path(current_album)

    return context
