#!/usr/bin/python3
""" Starts a Flash Web Application """
import os
from flask import Flask, render_template, redirect, request, url_for
from models.event import Event
from models import storage
from flask import session
from models.user import User
from .forms import CreateEventForm
from flask_wtf import csrf
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '575ea3040135364ec552de39befd1add'
app.config['UPLOAD_FOLDER'] = ''

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

def current_user():
    """current user session"""
    user_id = session.get('user_id')
    if user_id:
        user = storage.get(User, user_id)
        return user
    else:
        return None


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """ Creating event"""
    if not current_user():
        return redirect(url_for('signin'))

    form = CreateEventForm()
    csrf_token = csrf.generate_csrf()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        image_file = form.image.data
        venue = form.venue.data
        date_time = form.date_time.data

        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_path_str = str(image_path)
        else:
            image_path = None

        event = Event(
            title=title,
            description=description,
            image=image_path_str,
            venue=venue,
            date_time=date_time,
            slots_available=slots_available,
            user=current_user()
        )
        event.save()
        return redirect(url_for('profile'))
    else:
        print(form.errors)
        print(form.data)
    return render_template('create_event.html', form=form,
                           csrf_token=csrf_token)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
