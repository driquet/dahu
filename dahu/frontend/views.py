import os
from functools import wraps
from flask import Blueprint, current_app, abort, render_template, send_from_directory, request, session, url_for, redirect
from dahu.core import album, image, permission
from dahu.frontend import context, forms

frontend = Blueprint('frontend', __name__, template_folder='templates')

def render_theme(template, **kwargs):
    template_path = os.path.join(current_app.config['FRONTEND_THEME'], template)
    return render_template(template_path, **kwargs)

def get_argument(name):
    if request.args.get(name): return request.args.get(name)
    if name in session: return session[name]
    return ''

def login_required(f):
    @wraps(f)
    def decorated_function(album_path, *args, **kwargs):
        p_config = permission.get_config(current_app.config['CACHE_PATH'], 'permissions.json')

        if request.args.get('album_key'):
            session['album_key'] = request.args.get('album_key')
        album_key = session['album_key'] if session.has_key('album_key') else ''

        if not 'username' in session:
            if not permission.is_public_album(p_config, album_path) and \
            not permission.check_album_key(p_config, album_path, album_key):
                abort(404)

        return f(album_path, *args, **kwargs)
    return decorated_function


@frontend.errorhandler(404)
def page_not_found(e):
    return render_theme('404.html'), 404


@frontend.route('/login/', defaults={'album_path':''}, methods=['GET', 'POST'])
@frontend.route('/login/<path:album_path>', methods=['GET', 'POST'])
def login(album_path):
    if session.has_key('username'):
        return redirect(url_for('.show_album', album_path=album_path))
    form = forms.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        p_config = permission.get_config(current_app.config['CACHE_PATH'])
        if permission.check_user_pwd(p_config, form.username.data, form.password.data):
            session['username'] = request.form['username']
            return redirect(url_for('.show_album', album_path=album_path))
    return render_theme('login.html', album_path=album_path, form=form)


@frontend.route('/logout/')
def logout():
    if session.has_key('username'):
        session.pop('username', None)
    return redirect(url_for('.show_album'))



@frontend.route('/', defaults={'album_path':''})
@frontend.route('/albums/<path:album_path>')
@login_required
def show_album(album_path):
    if not album.is_valid_path(current_app.config['ALBUMS_PATH'], album_path):
        abort(404)

    album_context = context.generate_album_context(album_path)
    return render_theme('album.html', **album_context)


@frontend.route('/image/<path:album_path>/<filename>/', defaults={'size':None})
@frontend.route('/image/<path:album_path>/<filename>/<size>/')
@login_required
def get_image(album_path, filename, size=None):
    image_retrieved = image.get_image(current_app.config['ALBUMS_PATH'], current_app.config['CACHE_PATH'], album_path, filename, size)
    if image_retrieved:
        return send_from_directory(*image_retrieved)
    abort(404)


@frontend.route('/image/thumb/<path:album_path>/<filename>/')
@login_required
def get_thumb(album_path, filename):
    thumb_retrieved = image.get_image(current_app.config['ALBUMS_PATH'], current_app.config['CACHE_PATH'], \
        album_path, filename, current_app.config['PICTURE_THUMBNAIL_SIZE'], thumbnail=True)
    if thumb_retrieved:
        return send_from_directory(*thumb_retrieved)
    abort(404)


@frontend.route('/albums/thumb/<path:album_path>/')
@login_required
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
