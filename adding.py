# Neta Shiff
# Deal with addition picture- download shows et

# imports
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

from FaceRecognition import processingIMG, auth

# mongo
USERNAME = ''
client = MongoClient('mongodb://localhost:27017')

FaceRecDB = client['UserFaceRec_db']
bp = Blueprint('add', __name__, url_prefix='/adds')

# for different location run needed to change
project_path = "C:\\Users\\User\\Documents\\winter2023\\capstone\\FaceRecognition"

UPLOAD_FOLDER = project_path + "\\static\\Uploads"

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'}

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = project_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/addpicture')
def start():
    return render_template('add/oldresult.html')


@bp.route('/')
def index():
    return redirect(url_for('blog.index'))


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
            print("the file you chose is : " + filename)

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
            return redirect(url_for('add.AfterProcessing', filename=filename))
    return render_template('adding/addpicture.html')


# display picture after processing
@bp.route('/AfterProcessing/<filename>', methods=('GET', 'POST'))
@login_required
def AfterProcessing(filename):
    # processing the IMG
    names = processingIMG.finding_face(filename)
    print(names)
    IMG_detect = names[len(names) - 1]
    if request.method == "POST":
        file_path = project_path + "\\static\\Uploads\\" + filename
        # processingIMG.show2(file_path, False)

        # url_for('add.AfterProcessing', filename=project_path + "\\Uploads\\" + filename, name='my_name')
        # Give the file read and write permissions
        os.chmod(file_path, S_IREAD | S_IWRITE)
        print("start processing:" + file_path)

        # img= url_for(img_path)
        return redirect(url_for('add.Show_landmarks', face_array=names))
    return render_template('adding/AfterProcessing.html', user_image='Uploads/' + filename,
                           Face_detected='IMG_detect/' + IMG_detect)


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


# display picture after processing
@bp.route('/Show_landmarks/<face_array>', methods=('GET', 'POST'))
@login_required
def Show_landmarks(face_array):
    print(face_array)
    print(type(face_array))
    file_names_array=[]

    for file_name in face_array.split(', ')[:-1]:
        fixed_file_path = file_name.replace("[", "").replace("']", "").replace("'", "")
        file_names_array.append('Face_landmarks/'+fixed_file_path)
    for file_name in face_array.split(', '):
        fixed_file_path = file_name.replace("[", "").replace("']", "").replace("'", "")
        file_names_array.append('Face_landmarks/' + fixed_file_path)
    try:
        # define the filter to identify the document to update
        filter = {"_id": '643ea4a720cf878230a9907b'}

        # define the update operation to add a row to the "rows" array
        update = {"$push": {"Imgaes": {"face_cut_picture": file_names_array[len(file_names_array)-1],
            "face_keypoint_name": file_names_array[:len(file_names_array)-2],
            "Date Created": datetime.datetime.utcnow()}}}
        # update the document
        user_name= auth.get_logged_in_user()
        document_id = auth.get_document_id()
        filter = {"_id": document_id}
        print(user_name)
        print(filter)
        userCollection = FaceRecDB[user_name]
        document = userCollection.update_one(filter, update)
        print(document)
        print("insetred")
        print(FaceRecDB.list_collection_names())
    except IOError:
        error = f"Picture didnt saved in db."
    print(face_array)
    print(file_names_array)
    # processing the IMG
    if request.method == "POST":
        return redirect(url_for('blog.index'))

    # for i in face_array:
    #     face_array[i] = '/Face_landmarks' + face_array[i]

    return render_template('adding/Show_landmarks.html', Pictures=file_names_array)
