#!/usr/bin/python3
"""
Contains the blueprint for the API
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.events import *
from api.v1.views.index import *
from api.v1.views.reviews import *
from api.v1.views.reservations import *
from api.v1.views.users import *
