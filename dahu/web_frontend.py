from flask import Flask
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension
from frontend.views import frontend

# App related initialization
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(frontend, url_prefix=app.config['FRONTEND_PREFIX'])

# Session KVSession
session_store = DictStore()
KVSessionExtension(session_store, app)

if __name__ == '__main__':
    app.debug = True
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])
