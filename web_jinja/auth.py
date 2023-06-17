#!/usr/bin/python3
""" Starts a Flash Web Application """
import base64
import requests
from datetime import datetime
from flask_login import login_required
from flask import flash
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from models import storage
from models.user import User
import os
from models.reservation import Reservation
from models.review import Review
from models.event import Event
from .forms import CreateEventForm
from flask_wtf import csrf
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '575ea3040135364ec552de39befd1add'
app.config['UPLOAD_FOLDER'] = ''
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Loads the user object based on the user_id"""
    return storage.get(User, user_id)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup method"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(name=name, email=email, password=password)
        storage.new(user)
        storage.save()

        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """signin method"""
    form = SigninForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        users = storage.all(User)
        user = next((user for user in users.values() if user.email == email), None)

        if user and user.validate_password(password):
            session['user_id'] = user.id
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('signin.html', form=form)


def get_current_user():
    """Get current user"""
    user_id = session.get('user_id')
    if user_id:
        return storage.get(User, user_id)
    return None


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
                event['image_path'] = '/static/images/default.jpg'
            event['has_passed'] = datetime.strptime(event['date_time'], '%Y-%m-%dT%H:%M:%S') < datetime.now()
        return render_template('events.html', events=events)
    else:
        return render_template('error.html', message='Failed to retrieve events')


@app.route('/event/<event_id>')
def view_event(event_id):
    """Retrieve the event from the API using the event_id"""
    response = requests.get(f'http://0.0.0.0:5000/api/v1/events/{event_id}')
    if response.status_code == 200:
        event = response.json()
        event['has_passed'] = datetime.strptime(event['date_time'], '%Y-%m-%dT%H:%M:%S') < datetime.now()
        reviews_response = requests.get(f'http://0.0.0.0:5000/api/v1/events/{event_id}/reviews')
        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
            event['reviews'] = reviews
        else:
            event['reviews'] = []

        return render_template('event_page.html', event=event)
    else:
        return render_template('error.html', message='Failed to retrieve event')


@app.route('/reserve', methods=['POST'])
@login_required
def reserve_event():
    """Function that reserves a slot for a user"""
    user = get_current_user()
    if not user:
        return redirect(url_for('signin'))

    event_id = request.form.get('event_id')

    event = storage.get(Event, event_id)

    if event:
        if event.slots_available > 0:
            user_id = user.id
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


@app.route('/signout')
@login_required
def signout():
    """signout function"""
    session.pop('user_id', None)
    return redirect('/signin')


@app.route('/profile')
@login_required
def profile():
    """profile display"""
    user = current_user

    if user:
        return render_template('profile.html', user=user)

    return redirect('/signin')

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """ Creating event"""
    if not current_user:
        return redirect(url_for('signin'))

    form = CreateEventForm()
    csrf_token = csrf.generate_csrf()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        image_file = form.image.data
        venue = form.venue.data
        date_time = form.date_time.data
        slots_available = form.slots_available.data

        event = None

        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)

            with open(filepath, 'rb') as f:
                image_data = f.read()

            encoded_image = base64.b64encode(image_data).decode('utf-8')

            event = Event(
                title=title,
                description=description,
                image_file=filepath,
                venue=venue,
                date_time=date_time,
                slots_available=slots_available,
                user=current_user
            )
        else:
            event = Event(
                title=title,
                description=description,
                venue=venue,
                date_time=date_time,
                slots_available=slots_available,
                user=current_user
            )
        event.save()
        return redirect(url_for('profile'))
    else:
        print(form.errors)
        print(form.data)
    return render_template('create_event.html', form=form, csrf_token=csrf_token)


@app.route('/events/<event_id>/review', methods=['GET', 'POST'])
@login_required
def review_event(event_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            user_id = current_user.id
            review = Review(content=content, event_id=event_id, user_id=user_id)
            storage.new(review)
            storage.save()
            flash('Review submitted successfully!')
            return redirect(url_for('view_event', event_id=event_id))
        else:
            flash('Please enter a review before submitting.')

    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    return render_template('review.html', event=event)

if __name__ == "__main__":
    """Main Function"""
    app.run(host='0.0.0.0', port=5001)
