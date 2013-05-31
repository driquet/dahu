# -*- coding: utf-8 -*-

'''
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Deals with users and permissions (storage of password, checking if the user can see albums and so on)

The configuration files is a dict that contains :
    - users (name, password)
    - public albums
    - hash key for private albums
'''

import os, json
from dahu.core import authentication

def get_config(cache_dir, filename='permissions.json'):
    """ Read the users' configuration file """
    try:
        with open(os.path.join(cache_dir, filename)) as f:
            content = ''.join(f.readlines())
            return json.loads(content)
    except IOError:
        return {'users':{}, 'public':['/'], 'private_key':{}}


def save_config(config, cache_dir, filename='permissions.json'):
    with open(os.path.join(cache_dir, filename), 'w') as f:
        f.write(json.dumps(config))


# ---- FUNCTIONS RELATED TO PUBLIC ALBUMS ----
def is_public_album(config, album):
    return album == "" or album in config['public']

def set_album_public(config, album):
    if album not in config['public']:
        config['public'].append(album)

def set_album_private(config, album):
    if album in config['public']:
        config['public'].remove(album)


# ---- FUNCTIONS RELATED TO USERS ----
def check_user_pwd(config, user, pwd):
    if user in config['users']:
        return authentication.check_hash(pwd, config['users'][user])
    return False

def set_user_pwd(config, user, pwd):
    config['users'][user] = authentication.create_hash(pwd)

def del_user(config, user):
    config['users'].pop(user, None)


# ---- FUNCTIONS RELATED TO PRIVATE ALBUM (ACCESSED BY A KEY) ----
def generate_album_key(config, album):
    config['private_key'][album] = authentication.generate_album_key()

def get_album_key(config, album):
    if album not in config['private_key']:
        generate_album_key(config, album)
    return config['private_key'][album]

def check_album_key(config, album, key):
    if album not in config['private_key']:
        return False
    return config['private_key'][album] == key
