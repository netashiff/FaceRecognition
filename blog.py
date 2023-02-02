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

    return render_template('adding/index.html')
    #, folium_map=folium_map- for the map






#try to input the new jump
