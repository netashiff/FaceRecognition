import functools
import os
from stat import S_IREAD, S_IWRITE



from flask import (
    Blueprint, flash, Flask, g, redirect, render_template, request, session, url_for, Flask, send_from_directory
)

from pymongo import MongoClient
import datetime

from werkzeug.utils import secure_filename

from FaceRecognition.auth import login_required

USERNAME = ''
client = MongoClient('mongodb://localhost:27017')

FaceRecDB = client['UserFaceRec_db']
bp = Blueprint('add', __name__, url_prefix='/adds')

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\Uploads"

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'}

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/addpicture')
def start():
    return render_template('add/oldresult.html')


@bp.route('/')
def index():
    # start_coords = (25.775084, -80.1947)
    # folium_map = create_map_html(start_coords)

    return render_template('blog/index.html')
    # , folium_map=folium_map- for the map


# try to input the new jump
@bp.route('/newIMG', methods=('GET', 'POST'))
@login_required
def add_IMG():
    print("enter to print")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("the file you chosse is : " + filename)

            # Get username
            from FaceRecognition.auth import get_logged_in_user
            username = get_logged_in_user()

            try:
                IMGname = request.form['name']
                IMG_collection = FaceRecDB['OrifinalIMG']
                IMG_info = {
                    "username": username,
                    "img_name": IMGname,
                    "file_name": filename,
                    "Date Created": datetime.datetime.utcnow()}
                document = IMG_collection.insert_one(IMG_info).inserted_id
                print(FaceRecDB.list_collection_names())
            except IOError:
                error = f"Picture didnt saved in db."
            # savinf the file in the uploads folder
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('add.AfterProcessing', name=filename))
    return render_template('adding/addpicture.html')



# display picture after processing
@bp.route('/AfterProcessing/<filename>', methods=('GET', 'POST'))
@login_required
def AfterProcessing():
    # # Retrieving uploaded file path from session
    # img_file_path = session.get(os.path.dirname(os.path.abspath(__file__)) + "\\Uploads"+'\\abc.txt', None)
    # # Display image in Flask application web page
    # return render_template('show_image.html', user_image=img_file_path)
    #processingIMG.finding_face()

    file_path = os.path.dirname(os.path.abspath(__file__)) + "\\Uploads"+'\\abba.jpg'
    url_for('add.AfterProcessing', filename=file_path, name='my_name')

    # Give the file read and write permissions
    os.chmod(file_path, S_IREAD | S_IWRITE)
    img_path = os.path.dirname(os.path.abspath(__file__)) + "\\Uploads"
    #img= url_for(img_path)
    return render_template('adding/AfterProcessing.html', filename=file_path)
    return send_from_directory(img_path, file_path)
    #return render_template("adding/AfterProcessing.html", img_path=img_path)
    # full_filename = os.path.dirname(os.path.abspath(__file__)) + "\\Uploads"+'\\abc.txt'
    # print(full_filename)
    # return render_template("adding/AfterProcessing.html", user_image=full_filename)

# try to input the new jump
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

        # Get username
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
