import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from pymongo import MongoClient
import datetime

USERNAME = ''
client = MongoClient('mongodb://localhost:27017')

FaceRecDB = client['UserFaceRec_db']
bp = Blueprint('auth', __name__, url_prefix='/auth')
current_id ={}


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        age = request.form['age']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                userCollection = FaceRecDB[username]
                USERNAME = username
                information = {
                               "Username": username,
                               "Password": password,
                               "First Name": first_name,
                               "Last Name": last_name,
                               "EMail": email,
                               "Age": age,
                               "Date Created": datetime.datetime.utcnow()}
                document_id = userCollection.insert_one(information).inserted_id
                print(document_id)
                current_id[username]= document_id
                print(current_id)
                print(FaceRecDB.list_collection_names())
            except IOError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        USERNAME = ''

        #Check if user exists and get pass
        usercol = FaceRecDB[username]
        myquery = {"Username": username}
        mydoc = usercol.find(myquery)
        USERPASS = ''
        USERID = ''
        for document in usercol.find():
            USERNAME = document["Username"]
            USERPASS = document["Password"]
            break

        user = USERNAME
        passwordok = False
        if user != username:
            error = 'Incorrect username. '

        elif USERPASS == password:
            passwordok = True

        elif not passwordok:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = USERNAME
            return redirect(url_for('add'))

        flash(error)

    return render_template('auth/login.html')


# Checks if a user is logged in before any. If there is no user id, or it doesn't exit, g.user will be None
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id


def get_logged_in_user():
    return session.get('user_id')


def get_document_id():
    return current_id[session.get('user_id')]


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('add'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view