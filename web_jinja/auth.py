#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import flash
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from models import storage
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = '575ea3040135364ec552de39befd1add'
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
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    """signout function"""
    session.pop('user_id', None)
    return redirect('/signin')


@app.route('/profile')
def profile():
    """profile display"""
    if 'user_id' in session:
        user_id = session['user_id']
        user = storage.get(User, user_id)

        if user:
            return render_template('profile.html', user=user)

    return redirect('/signin')


if __name__ == "__main__":
    """Main Function"""
    app.run(host='0.0.0.0', port=5001)
