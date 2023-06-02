#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
from models import storage
from models.event import Event
from flask import Flask, render_template, request
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/events')
def display_events():
    """Retrieve the first 9 events from the API"""
    response = requests.get('http://0.0.0.0:5000/api/v1/events')
    if response.status_code == 200:
        events = response.json()

        for event in events:
            if event['image'] is not None:
                event['image_path'] = '/static/images/' + event['image']
            else:
                event['image_path'] = '/static/images/default.jpg'  # Provide a default image path

        return render_template('events.html', events=events)
    else:
        return render_template('error.html', message='Failed to retrieve events')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
