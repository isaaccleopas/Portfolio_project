from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image')
    venue = StringField('Venue', validators=[DataRequired()])
    date_time = DateTimeField('Date and Time', validators=[DataRequired()])
    slots_available = IntegerField('Slots Available', validators=[DataRequired()])
