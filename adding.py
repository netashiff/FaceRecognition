import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from pymongo import MongoClient
import datetime

USERNAME = ''
client = MongoClient('mongodb://localhost:27017')

FaceRecognize = client['FaceRecognize']
bp = Blueprint('add', __name__, url_prefix='/adds')

