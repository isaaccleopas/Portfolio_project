from flask import Blueprint
from .events import events_bp
from .create_event import create_event_bp

app_views = Blueprint('app_views', __name__, template_folder='templates')

from .auth import *
from .event_page import *
from .events import *
from .event_reservation import *
from .create_event import create_event_routes

def register(app, options=None):
    app.register_blueprint(auth_bp, **options)
    app.register_blueprint(event_page_bp, **options)
    app.register_blueprint(events_bp, **options)
    app.register_blueprint(create_event_bp, **options)
    app.register_blueprint(event_reservation_bp, **options)
