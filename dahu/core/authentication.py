#!/user/bin/env python
# -*- coding: utf-8 -*-

'''
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Provides functions to deal with authentication
Source: https://exyr.org/2011/hashing-passwords/
'''

import hashlib, uuid
from os import urandom
from base64 import b64encode, b64decode
from itertools import izip
from pbkdf2 import pbkdf2_bin

# PBKDF2 parameters
SALT_LENGTH   = 12
KEY_LENGTH    = 24
HASH_FUNCTION = 'sha256'
COST_FACTOR   = 10000

# Albums' key parameters
ALBUM_KEY_LENGTH = 64

def create_hash(password):
    """ Generate a random salt and return a new hash for the password """
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = b64encode(urandom(SALT_LENGTH))
    return 'PBKDF2${}${}${}${}'.format(
        HASH_FUNCTION,
        COST_FACTOR,
        salt,
        b64encode(pbkdf2_bin(password, salt, COST_FACTOR, KEY_LENGTH,
            getattr(hashlib, HASH_FUNCTION))))


def check_hash(password, hash_):
    """ Check a password against an existing hash """
    if isinstance(password, unicode):
            password = password.encode('utf-8')

    algorithm, hash_function, cost_factor, salt, hash_a = hash_.split('$')
    assert algorithm == 'PBKDF2'

    hash_a = b64decode(hash_a)
    hash_b = pbkdf2_bin(password, salt, int(cost_factor), len(hash_a),
                        getattr(hashlib, hash_function))
    assert len(hash_a) == len(hash_b)

    diff = 0
    for char_a, char_b in izip(hash_a, hash_b):
        diff |= ord(char_a) ^ ord(char_b)
    return diff == 0


def generate_album_key():
    key = uuid.uuid4()
    return key.hex

if __name__ == '__main__':
    password = 'test1234'
    hash_pwd = create_hash(password)

    print hash_pwd
    print check_hash('test1234_', hash_pwd)
    print check_hash('test1234', hash_pwd)
