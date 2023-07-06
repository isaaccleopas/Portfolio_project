#!/usr/bin/python3
"""Contains a Flask web application API"""
import logging
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='web_jinja/templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'web_jinja/static/images'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.url_map.strict_slashes = False
db = SQLAlchemy()
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

login_manager = LoginManager(app)
login_manager.init_app(app)

from web_jinja.routes import routes_bp
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run()
