#!/usr/bin/python3
"""Contains a Flask web application API"""
import json
import requests
from datetime import datetime
from flask_login import login_required
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from models import storage
from models.user import User
from models.reservation import Reservation
from models.review import Review
from models.event import Event
from flask_wtf import csrf
from werkzeug.utils import secure_filename
import os
from flask import after_this_request
from flask import Flask, jsonify
from flask_cors import CORS
from web_jinja.routes import signin, signup, signout, profile
from models import storage
from api.v1.views import app_views

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = ''
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.environ.get('MY_APP_SECRET_KEY')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

def teardown_flask(exception):
    """ Flask app event listener"""
    storage.close()

@app.errorhandler(404)
def error_404(error):
    """Handles the error code 404"""
    return jsonify(error='not found'), 404


@app.errorhandler(400)
def error_400(error):
    """Handles the error code 400"""
    msg = "Bad request"
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
