#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
from models import storage
from models.event import Event
from models.reservation import Reservation
from flask import Flask, render_template, request, current_user, login_required
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()



@app.route('/reserve', methods=['POST'])
@login_required
def reserve_event():
    """Function that reserves a slot for a user"""
    event_id = request.form.get('event_id')

    event = storage.get(Event, event_id)

    if event:
        if event.slots_available > 0:
            user_id = current_user.id
            slots_reserved = 1
            reservation = Reservation(user_id=user_id, event_id=event_id,
                                      slots_reserved=slots_reserved)
            storage.new(reservation)
            storage.save()
            event.slots_available -= slots_reserved
            storage.save()
            return redirect(f'/event/{event_id}')
        else:
            return render_template('error.html', message='No slots available')
    else:
        return render_template('error.html', message='Failed to retrieve event')

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
