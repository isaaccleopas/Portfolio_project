#!/usr/bin/python3
"""Contains a Flask web application API"""
import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__, template_folder='web_jinja/Templates')
app.config['SECRET_KEY'] = os.environ.get('MY_APP_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'web_jinja/static/images'
app.url_map.strict_slashes = False

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

login_manager = LoginManager()
login_manager.init_app(app)

from web_jinja.routes import routes_bp
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
