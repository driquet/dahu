#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Run the web frontend
'''

import argparse, os
from flask import Flask
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension
from dahu.frontend.views import frontend



def main():
    parser = argparse.ArgumentParser(description='Dahu web frontend')
    parser.add_argument('config', help='Dahu configuration file (default: config.py)')
    args = parser.parse_args()

    # App related initialization
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), args.config))
    app.register_blueprint(frontend, url_prefix=app.config['FRONTEND_PREFIX'])

    # Session KVSession
    session_store = DictStore()
    KVSessionExtension(session_store, app)

    app.debug = True
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])

if __name__ == '__main__':
    main()
