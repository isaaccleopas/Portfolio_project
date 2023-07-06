#!/usr/bin/python3
"""Contains a Flask web application API"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
