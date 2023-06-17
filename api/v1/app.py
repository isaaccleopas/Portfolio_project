#!/usr/bin/python3
"""Contains a Flask web application API"""
import os
from flask import after_this_request
from flask import Flask, jsonify
from flask_cors import CORS
from web_jinja.auth import signin, signup, signout, profile
from models import storage
from api.v1.views import app_views

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '575ea3040135364ec552de39befd1add'
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

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(400)
def error_400(error):
    """Handles the error code 400"""
    msg = "Bad request"
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
