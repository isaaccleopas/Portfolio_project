#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
from models import storage
from models.event import Event
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/event/<event_id>')
def view_event(event_id):
    """Retrieve the event from the API using the event_id"""
    response = requests.get(f'http://0.0.0.0:5000/api/v1/events/{event_id}')
    if response.status_code == 200:
        event = response.json()
        return render_template('event_page.html', event=event)
    else:
        return render_template('error.html', message='Failed to retrieve event')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
