import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_uploads import UploadSet, IMAGES
from pymongo import MongoClient
import datetime

from FaceRecognition.auth import login_required
from FaceRecognition.foliummaps import create_map_html

USERNAME = ''
client = MongoClient('mongodb://localhost:27017')

FaceRecognize = client['FaceRecognize']
bp = Blueprint('add', __name__, url_prefix='/adds')

UPLOAD_FOLDER = os.path.normpath(os.getcwd() + os.sep + os.pardir)+"\\Uploads"

ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}

@bp.route('/addpicture')
def start():
    return render_template('add/oldresult.html')


@bp.route('/')
def index():

    # start_coords = (25.775084, -80.1947)
    # folium_map = create_map_html(start_coords)

    return render_template('blog/index.html')
    #, folium_map=folium_map- for the map


#try to input the new jump
@bp.route('/newIMG', methods=('GET', 'POST'))
@login_required
def add_IMG():
    if request.method == 'POST':
        title = request.form['name']
        jump_number = request.form['jumpnumber']
        location = request.form['location']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        Partners = request.form['Partners']
        Dive_date = request.form['Dive_date']
        color = request.form['colors']
        #reccomendation = request.form['reccomendation']
        img = request.form['img']

        error = None

        #Get username
        from FaceRecognition.auth import get_logged_in_user
        username = get_logged_in_user()

        if not username:
            username = 'username is required.'

        # if error is None:
        #     try:
        #         print(username)
        #     except IntegrityError:
        #         error = f"username {username} is already registered."
        #     else:
        #         return redirect(url_for("blog.index"))
        #
        # flash(error)

    return render_template('adding/addpicture.html')



#try to input the new jump
@bp.route('/OldResults', methods=('GET', 'POST'))
@login_required
def old_results():
    if request.method == 'POST':
        # title = request.form['name']
        # jump_number = request.form['jumpnumber']
        # location = request.form['location']
        # latitude = request.form['latitude']
        # longitude = request.form['longitude']
        # Partners = request.form['Partners']
        # Dive_date = request.form['Dive_date']
        # color = request.form['colors']
        # #reccomendation = request.form['reccomendation']
        img = request.form['img']
        error = None

        #Get username
        from FaceRecognition.auth import get_logged_in_user
        username = get_logged_in_user()

        # if not username:
        #     username = 'username is required.'
        #
        # if error is None:
        #     try:
        #         print(username)
        #         userJumpsCollection = jumpMapDB[str(username)]
        #         DZ_info = {"Name": title,
        #                    "Jump Number": jump_number,
        #                     "Location": location,
        #                    "Latitude": latitude,
        #                    "Longitude": longitude,
        #                    "Partners": Partners,
        #                    "Dive_date": Dive_date,
        #                    "Color": color,
        #                    "img": img}
        #                    #, "Date Created": datetime.datetime.utcnow()
        #         document = userJumpsCollection.insert_one(DZ_info).inserted_id
        #         print(jumpMapDB.list_collection_names())

        #     except IOError:
        #         error = f"username {username} is already registered."
        #     else:
        #         return redirect(url_for("blog.index"))
        #
        # flash(error)

    return render_template('adding/oldresult.html')