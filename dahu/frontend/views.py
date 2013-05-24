import os
from flask import Blueprint, current_app, abort, render_template, send_from_directory
from dahu.core import album, image
from dahu.frontend import context

frontend = Blueprint('frontend', __name__, template_folder='templates')

def render_theme(template, **kwargs):
    template_path = os.path.join(current_app.config['FRONTEND_THEME'], template)
    return render_template(template_path, **kwargs)


@frontend.route('/', defaults={'album_path':''})
@frontend.route('/albums/<path:album_path>')
def show_album(album_path):
    if not album.is_valid_path(current_app.config['ALBUMS_PATH'], album_path):
        abort(404)

    album_context = context.generate_album_context(album_path)
    return render_theme('album.html', **album_context)


@frontend.route('/image/<path:album_path>/<filename>/', defaults={'size':None})
@frontend.route('/image/<path:album_path>/<filename>/<size>/')
def get_image(album_path, filename, size=None):
    image_retrieved = image.get_image(current_app.config['ALBUMS_PATH'], current_app.config['CACHE_PATH'], album_path, filename, size)
    if image_retrieved:
        return send_from_directory(*image_retrieved)
    abort(404)


@frontend.route('/image/thumb/<path:album_path>/<filename>/')
def get_thumb(album_path, filename):
    thumb_retrieved = image.get_image(current_app.config['ALBUMS_PATH'], current_app.config['CACHE_PATH'], \
        album_path, filename, current_app.config['PICTURE_THUMBNAIL_SIZE'], thumbnail=True)
    if thumb_retrieved:
        return send_from_directory(*thumb_retrieved)
    abort(404)


@frontend.route('/albums/thumb/<path:album_path>/')
def get_album_thumb(album_path):
    album_thumb = album.get_album_thumbnail(current_app.config['ALBUMS_PATH'], current_app.config['CACHE_PATH'], \
        album_path, current_app.config['ALBUM_THUMBNAIL_SIZE'])
    if album_thumb:
        return send_from_directory(*album_thumb)
    abort(404)


@frontend.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join(frontend.root_path, 'templates', current_app.config['FRONTEND_THEME'], 'static')
    return send_from_directory(static_path, filename)
