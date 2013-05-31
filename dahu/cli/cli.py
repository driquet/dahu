#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    This file provides a Command Line Interface
"""

from cmd2 import Cmd
from getpass import getpass
from dahu.core import cache, permission

def load_config(filename):
    config = {}
    execfile(filename, {}, config)
    return config


class DahuCLI(Cmd):
    """
    This CLI provides the same action than the web frontend, plus administrative action
    Actions are :
        - albums:
            - display albums (ls,tree)
            - display pictures
            - thumbnail (get/set)
            - permission (get/set)
            - description (get/set)
            - direct link (get/generate)
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



if __name__ == '__main__':
    config = '/Users/driquet/git/dahu/dahu/config.py'
    DahuCLI(load_config(config)).cmdloop()
