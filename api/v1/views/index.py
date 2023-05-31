
#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route('/stats',
                 methods=['GET'], strict_slashes=False)
def stat():
    """returns the number of each objects by type"""
    return jsonify(
        events=storage.count('Event'),
        reservations=storage.count('Reservation'),
        reviews=storage.count('Review'),
        users=storage.count('User')
    )
