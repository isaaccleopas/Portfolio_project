#!/usr/bin/python3
""" Starts a Flash Web Application """
import base64
import requests
import models
from flask import current_app
from datetime import datetime
from flask import flash
from flask import session
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_login import login_user, login_required, logout_user, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from models.engine.db_storage import DBStorage
from models.user import User
import os
from .forms import CreateEventForm
from models.reservation import Reservation
from models.review import Review
from models.event import Event
from flask_wtf import csrf
from werkzeug.utils import secure_filename

storage = DBStorage()
storage.reload()

routes_bp = Blueprint('routes', __name__)

from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    """Loads the user object based on the user_id"""
    return storage.get(User, user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please sign in to access this page.', 'error')
    return redirect(url_for('routes.signin'))

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

@routes_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup method"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(name=name, email=email, password=password)
        storage.new(user)
        storage.save()

        return redirect(url_for('routes.signin'))

    return render_template('signup.html')

@routes_bp.route('/signin', methods=['GET', 'POST'])
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
            return redirect(url_for('routes.profile'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('signin.html', form=form)


def get_current_user():
    """Get current user"""
    user_id = session.get('user_id')
    if user_id:
        return storage.get(User, user_id)
    return None

@routes_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """ Creating event"""
    if not current_user.is_authenticated:
        return redirect(url_for('routes.signin'))

    form = CreateEventForm()
    csrf_token = csrf.generate_csrf()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        image_file = form.image.data
        venue = form.venue.data
        date_time = datetime.combine(form.date.data, form.time.data)
        slots_available = form.slots_available.data

        event = None

        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join('web_jinja/static/images/', filename)
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
                user=current_user._get_current_object()
            )
        else:
            event = Event(
                title=title,
                description=description,
                venue=venue,
                date_time=date_time,
                slots_available=slots_available,
                user=current_user._get_current_object()
            )
        storage.new(event)
        storage.save()
        return redirect(url_for('routes.profile'))
    else:

        return render_template('create_event.html', form=form)

@routes_bp.route('/event/<event_id>')
def view_event(event_id):
    """Retrieve the event from the API using the event_id"""
    response = requests.get(f'https://portfolioproject-production-496e.up.railway.app/api/v1/events/{event_id}')
    if response.status_code == 200:
        event = response.json()
        event['has_passed'] = datetime.strptime(event['date_time'], '%Y-%m-%dT%H:%M:%S') < datetime.now()
        reviews_response = requests.get(f'https://portfolioproject-production-496e.up.railway.app/api/v1/events/{event_id}/reviews')
        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
            event['reviews'] = reviews
        else:
            event['reviews'] = []

        return render_template('event_page.html', event=event)
    else:
        return render_template('error.html', message='Failed to retrieve event')

@routes_bp.route('/')
def home():
    """Retrieve events from the API"""
    response = requests.get('https://portfolioproject-production-496e.up.railway.app/api/v1/events')
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if event['image'] is not None:
                event['image_path'] = '/static/images/' + event['image']
            else:
                event['image_path'] = '/static/images/default.jpg'
            event['has_passed'] = datetime.strptime(event['date_time'], '%Y-%m-%dT%H:%M:%S') < datetime.now()
        return render_template('home.html', events=events)
    else:
        return render_template('error.html', message='Failed to retrieve events')

@routes_bp.route('/events/<event_id>/review', methods=['GET', 'POST'])
@login_required
def review_event(event_id):
    """Review event"""
    if not current_user.is_authenticated:
        return redirect(url_for('routes.signin'))

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            user_id = current_user.id
            review = Review(content=content, event_id=event_id, user_id=user_id)
            storage.new(review)
            storage.save()
            flash('Review submitted successfully!')
            return redirect(url_for('routes.view_event', event_id=event_id))
        else:
            flash('Please enter a review before submitting.')

    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    return render_template('review.html', event=event)

@routes_bp.route('/reserve', methods=['POST'])
@login_required
def reserve_event():
    """Function that reserves a slot for a user"""
    if not current_user.is_authenticated:
        return redirect(url_for('routes.signin'))

    user_id = current_user.id

    event_id = request.form.get('event_id')

    event = storage.get(Event, event_id)

    if event:
        if event.slots_available > 0:
            slots_reserved = 1
            reservation = Reservation(user_id=user_id, event_id=event_id,
                                      slots_reserved=slots_reserved)
            storage.new(reservation)
            storage.save()
            event = storage.session.merge(event)
            event.slots_available -= slots_reserved
            storage.save()
            return redirect(f'/event/{event_id}')
        else:
            return render_template('error.html', message='No slots available')
    else:
        return render_template('error.html', message='Failed to retrieve event')

@routes_bp.route("/search", methods=["GET"])
def search_events():
    """Searches events based on title and venue"""
    query = request.args.get("query", "").lower()
    results = []

    if query:
        events = models.storage.all(Event).values()
        results = [event for event in events if query in getattr(event, "title", "").lower() or query in getattr(event, "venue", "").lower()]

    return render_template("search_results.html", results=results)

@routes_bp.route('/profile')
@login_required
def profile():
    """profile display"""
    if not current_user.is_authenticated:
        return redirect(url_for('routes.signin'))

    user = current_user

    if user:
        return render_template('profile.html', user=user)

    return redirect('/signin')

@routes_bp.route('/signout')
@login_required
def signout():
    """signout function"""
    if not current_user.is_authenticated:
        return redirect(url_for('routes.signin'))

    session.pop('user_id', None)
    return redirect('/signin')
