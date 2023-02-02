from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from FaceRecognition.auth import login_required
from FaceRecognition.foliummaps import create_map_html
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
jumpMapDB = client['JumpMap']
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():

    # start_coords = (25.775084, -80.1947)
    # folium_map = create_map_html(start_coords)

    return render_template('blog/index.html')
    #, folium_map=folium_map- for the map

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
    return render_template('blog/create.html')

# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()
#
#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")
#
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
#
#     return post

#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
# def update(id):
#
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None
#
#         if not title:
#             error = 'Title is required.'
#
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))
#
#     return render_template('blog/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))




#try to input the new jump