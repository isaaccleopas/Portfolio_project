#!/usr/bin/python3
"""Contains a Flask web application API"""
import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
"""Flask web application instances"""
app_host = os.getenv('EVENT_API_HOST', '0.0.0.0')
app_port = int(os.getenv('EVENT_API_PORT', '5000'))
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
    app_host = os.getenv('EVENT_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('EVENT_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )

