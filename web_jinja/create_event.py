#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template, redirect, request, url_for
from models.event import Event
from utils import current_user
from models import storage
from flask import session
from models.user import User

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

def current_user():
    """current user session"""
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return user
    else:
        return None

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """ Creating event"""
    if not current_user:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.form.get('image')
        venue = request.form.get('venue')
        date_time = request.form.get('date_time')
        slots_available = request.form.get('slots_available')

        event = Event(
            title=title,
            description=description,
            image=image,
            venue=venue,
            date_time=date_time,
            slots_available=slots_available,
            user=current_user
        )
        event.save()
        return redirect(url_for('profile'))

    return render_template('create_event.html')

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
