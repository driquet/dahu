from flask import Flask
from frontend.views import frontend

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(frontend, url_prefix=app.config['FRONTEND_PREFIX'])

if __name__ == '__main__':
    app.debug = True
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])
