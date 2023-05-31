#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
from models import storage
from models.event import Event
from models.reservation import Reservation
from flask import Flask, render_template, request
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/reserve', methods=['POST'])
def reserve_event():
    """function that reserves a slot for a user"""
    event_id = request.form.get('event_id')
    response = requests.get(f'http://localhost:5000/api/v1/events/{event_id}')
    if response.status_code == 200:
        event = response.json()
        if event['slots_available'] > 0:
            user_id = 'your_user_id'  # Set the user_id based on the currently logged-in user
            slots_reserved = 1  # Set the number of slots to reserve (e.g., 1)
            reservation_data = {
                'user_id': user_id,
                'event_id': event_id,
                'slots_reserved': slots_reserved
            }
            reservation_response = requests.post('http://localhost:5000/api/v1/reservations',
                                                 json=reservation_data)
            if reservation_response.status_code == 201:
                event['slots_available'] -= slots_reserved
                update_response = requests.put(f'http://localhost:5000/api/v1/events/{event_id}',
                                               json=event)
                if update_response.status_code == 200:
                    return redirect(f'/event/{event_id}')
                else:
                    return render_template('error.html', message='Failed to update event')
            else:
                return render_template('error.html', message='Failed to create reservation')
        else:
            return render_template('error.html', message='No slots available')
    else:
        return render_template('error.html', message='Failed to retrieve event')



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
