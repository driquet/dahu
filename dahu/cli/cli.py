#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides a Command Line Interface
"""

import os
from cmd2 import Cmd
from getpass import getpass
from dahu.core import album, cache, permission

def load_config(filename):
    config = {}
    execfile(filename, {}, config)
    return config


class DahuCLI(Cmd):
    """
    This CLI provides the same action than the web frontend, plus administrative action
    Actions are :
        - albums:
            - display albums
            (- thumbnail (get/set))
            - permission (get/set)
            (- description (get/set))
            (- direct link (get/generate))
        - cache:
            - clean
            - update
        - users:
            - display all users
            - users (new/edit/del)
    """

    def __init__(self, config):
        Cmd.__init__(self)
        self.config = config

    def do_EOF(self, line):
        return True

    def query_yes_no(self, question, default="yes"):
        valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
        if default == None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            self.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                self.poutput("Please respond with 'yes' or 'no' (or 'y' or 'n').")

    # ---- Users ----
    def do_userlist(self, arg):
        perm_config = permission.get_config(self.config['CACHE_PATH'])
        for user in perm_config['users']:
            self.poutput(user)


    def do_useradd(self, arg):
        user = raw_input("username: ")
        pwdprompt = lambda: (getpass(), getpass('Retype password: '))

        p1, p2 = pwdprompt()
        while p1 != p2:
            self.poutput('Passwords do not match. Try again.\n')
            p1, p2 = pwdprompt()

        perm_config = permission.get_config(self.config['CACHE_PATH'])
        permission.set_user_pwd(perm_config, user, p1)
        permission.save_config(perm_config, self.config['CACHE_PATH'])


    def do_userdel(self, arg):
        perm_config = permission.get_config(self.config['CACHE_PATH'])
        if arg in perm_config['users']:
            choice = self.query_yes_no("Delete user %s. Are you sure ?" % arg, default="no")
            if choice:
                permission.del_user(perm_config, arg)
                permission.save_config(perm_config, self.config['CACHE_PATH'])
        else:
            self.poutput('User not found\n')


    # ---- Cache ----
    def do_cache(self, arg):
        if arg == 'clear':
            choice = self.query_yes_no("Clean cache. Are you sure ?", default="no")
            if choice:
                cache.clear_cache(self.config['CACHE_PATH'], verbose=True)

        elif arg == 'update':
            self.poutput('This operation could take several minute ...')
            cache.update_cache(self.config['ALBUMS_PATH'], self.config['CACHE_PATH'], '', self.config['ALBUM_THUMBNAIL_SIZE'], \
                               [(self.config['PICTURE_THUMBNAIL_SIZE'], True), (self.config['PICTURE_SLIDESHOW_SIZE'], False)], \
                               verbose=True)
            self.poutput('Cache update done !')

        else:
            pass


    # ---- Albums ----
    def do_permission(self, arg):
        args = arg.split()
        if len(args) == 1:
            # Only one argument: name of an album
            # Print the permission of the album (if it exists)
            if album.is_valid_path(self.config['ALBUMS_PATH'], arg):
                perm_config = permission.get_config(self.config['CACHE_PATH'])
                if arg in perm_config['public']:
                    self.poutput('public album')
                else:
                    self.poutput('private album')

            else:
                self.perror("Invalid album name")

        elif len(args) == 2:
            # Two arguments: name of an album + associated permission
            album_path = args[0]
            album_perm = args[1]

            if album.is_valid_path(self.config['ALBUMS_PATH'], album_path):
                if album_perm in ['private', 'public']:
                    perm_config = permission.get_config(self.config['CACHE_PATH'])
                    if album_perm == 'private':
                        permission.set_album_private(perm_config, album_path)
                    elif album_perm == 'public':
                        permission.set_album_public(perm_config, album_path)
                    permission.save_config(perm_config, self.config['CACHE_PATH'])

                else:
                    self.perror("Invalid permission (must be 'public' or 'private')")
            else:
                self.perror("Invalid album name")

        else:
            pass


    def do_ls(self, arg):
        if album.is_valid_path(self.config['ALBUMS_PATH'], arg):
            inner_albums = album.get_album_dirs(self.config['ALBUMS_PATH'], arg)
            inner_pictures = album.get_album_pictures(self.config['ALBUMS_PATH'], arg)

            for inner_album in inner_albums:
                self.poutput("%s/  (%d picture(s))" % (inner_album, album.get_album_total_number_pictures(self.config['ALBUMS_PATH'], os.path.join(arg, inner_album))))

            for inner_picture in inner_pictures:
                self.poutput("%s" % inner_picture)

        else:
            self.perror("Invalid album name")


    def do_keygen(self, arg):
        if arg and album.is_valid_path(self.config['ALBUMS_PATH'], arg):
            perm_config = permission.get_config(self.config['CACHE_PATH'])
            permission.generate_album_key(perm_config, arg)
            key = permission.get_album_key(perm_config, arg)
            permission.save_config(perm_config, self.config['CACHE_PATH'])

            print 'Key for album "%s" has been generated: %s' % (arg, key)

        else:
            self.perror("Invalid album name")

    def do_directlink(self, arg):
        if arg and album.is_valid_path(self.config['ALBUMS_PATH'], arg):
            perm_config = permission.get_config(self.config['CACHE_PATH'])
            key = permission.get_album_key(perm_config, arg)
            permission.save_config(perm_config, self.config['CACHE_PATH'])

            print permission.get_album_direct_link(perm_config, arg, self.config['FRONTEND_HOST'], \
                                                   self.config['FRONTEND_PORT'], self.config['FRONTEND_PREFIX'])

        else:
            self.perror("Invalid album name")




if __name__ == '__main__':
    config = '/Users/driquet/git/dahu/dahu/config.py'
    DahuCLI(load_config(config)).cmdloop()
