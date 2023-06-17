#!/usr/bin/python3
"""
This module handles all default RestFul API actions for Events.
"""
from flask import abort, jsonify, request
from models import storage
from models.event import Event
from api.v1.views import app_views


@app_views.route('/events', methods=['GET'], strict_slashes=False)
def get_events():
    """
    Retrieves the list of all Event objects.
    """
    events = storage.all(Event).values()
    return jsonify([event.to_dict() for event in events])


@app_views.route('/events/<event_id>', methods=['GET'], strict_slashes=False)
def get_event(event_id):
    """
    Retrieves an Event object with associated reviews.
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)
    return jsonify(event.to_dict(include_reviews=True))


@app_views.route('/events/<event_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_event(event_id):
    """
    Deletes an Event object.
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)
    storage.delete(event)
    storage.save()
    return jsonify({}), 200


@app_views.route('/events', methods=['POST'], strict_slashes=False)
def create_event():
    """
    Creates a new Event object.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    title = req_data.get('title')
    description = req_data.get('description')
    image = req_data.get('image')
    venue = req_data.get('venue')
    date_time = req_data.get('date_time')
    slots_available = req_data.get('slots_available')
    if not title or not description or not image or not venue or not date_time or not slots_available:
        abort(400, "Missing required fields")
    event = Event(title=title, description=description, image=image, venue=venue,
                  date_time=date_time, slots_available=slots_available)
    storage.new(event)
    storage.save()
    return jsonify(event.to_dict()), 201


@app_views.route('/events/<event_id>', methods=['PUT'], strict_slashes=False)
def update_event(event_id):
    """
    Updates an Event object.
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        setattr(event, k, v)
    storage.save()
    return jsonify(event.to_dict()), 200
