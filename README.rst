Dahu
====

Dahu is a picture gallery based on the directory tree of your digital albums.

- No database needed
- Automatic generation of thumbnails without editing original files
- Include a CLI to manage albums and a web frontend
- Permission management: an album can be public or private or shared by a link

Dahu uses:

- `Flask <http://flask.pocoo.org/>`__, a Python microframework
- `Bootstrap <http://twitter.github.io/bootstrap/index.html>`__
- `YoxView <http://www.yoxigen.com/yoxview/>`__, a jQuery plugin to display pictures

Demo
----
You will find here a demo (soon enough).


Features
--------

- No database needed
- Non-destructive picture transformation
- Album permissions (public or private)
- Share albums with a direct link
- Upload your albums using your favorite synchronization tool (ssh, rsync, etc.)
- Gallery based on directory tree
- Web frontend to expose your gallery
- CLI to manage your albums
- Download a whole album from the web frontend (soon)
- Theming support


Installation
------------

Requirements
############
Dahu requires some Python modules to be installed.
Using pip, you can install them as follow:

::

    $ pip install -r requirements.txt

Setting up Dahu
###############
Dahu uses two main files:

- ``config.py``: contains data related to your application (where are stored picture, where to cache pictures, and so on)
- ``permissions.json``: automatically generated, that contains album permissions

To set up Dahu, you need to:

1. Install requirements
2. Customize the ``config.py`` file
3. Create the cache directory (don't forget, it needs to be readable/writable)
4. Deploy the application (see `Deployment`_ section)


Configuration
-------------

Dahu configuration
##################
Configuration of Dahu takes place in the ``config.py`` file.
Options are self-explicit so you won't find any description of them here.

Dealing with permissions
########################
Permissions are stored in the file ``permissions.json``, located in the cache directory. It contains:

- Users (password encryped using PBKDF2 with salt)
- Public/Private albums
- Album keys for direct links

To manage these data, you can use Dahu CLI.
Launch the CLI with:

::

    $ python dahu -c


=====================================   ===========
Command                                 Description
=====================================   ===========
userlist                                List registered users
useradd                                 Add/Edit an user
userdel [user]                          Remove an user
permission [album] [private/public]     Manage (get or set) permission for an album
keygen [album]                          Generate an album key
directlink [album]                      Return the direct link for an album
ls [album]                              List the content of an album
cache [update/clear]                    Update or clear thumbnails
=====================================   ===========

Deployment
----------

Security
--------

Enhancements
------------
A lot of enhancements can be done. Feel free to contribute by:
- reporting issues
- proposing new features
- enhancing Dahu

Possible enhancement are:
- admin frontend

Troubles
--------

Licence
-------
BSD Licence. See LICENCE file.
