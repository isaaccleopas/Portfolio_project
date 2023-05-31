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


@app.route('/more-events', methods=['GET'])
def more_events():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 9))
    events = Event.query.offset((page - 1) * per_page).limit(per_page).all()

    return render_template('event_page.html', events=events)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
