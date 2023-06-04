#!/usr/bin/python3
"""
This module handles all default RestFul API actions for Reservations.
"""
from flask import abort, jsonify, request
from models import storage
from models.event import Event
from models.user import User
from models.reservation import Reservation
from api.v1.views import app_views


@app_views.route('/reservations', methods=['GET'],
                 strict_slashes=False)
def get_reservations():
    """
    Retrieves the list of all Reservation objects.
    """
    reservations = storage.all(Reservation).values()
    return jsonify([reservation.to_dict() for reservation in reservations])


@app_views.route('/reservations/<reservation_id>', methods=['GET'],
                 strict_slashes=False)
def get_reservation(reservation_id):
    """
    Retrieves a Reservation object.
    """
    reservation = storage.get(Reservation, reservation_id)
    if not reservation:
        abort(404)
    return jsonify(reservation.to_dict())


@app_views.route('/reservations/<reservation_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reservation(reservation_id):
    """
    Deletes a Reservation object.
    """
    reservation = storage.get(Reservation, reservation_id)
    if not reservation:
        abort(404)
    storage.delete(reservation)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reservations', methods=['POST'],
                 strict_slashes=False)
def create_reservation():
    """
    Creates a new Reservation object.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    event_id = req_data.get('event_id')
    user_id = req_data.get('user_id')
    slots_reserved = req_data.get('slots_reserved')
    if not event_id or not user_id or not slots_reserved:
        abort(400, "Missing required fields")
    event = storage.get(Event, event_id)
    user = storage.get(User, user_id)
    if not event:
        abort(404)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    reservation = Reservation(event_id=event_id, user_id=user_id,
                              slots_reserved=slots_reserved)
    storage.new(reservation)
    storage.save()
    return jsonify(reservation.to_dict()), 201


@app_views.route('/reservations/<reservation_id>', methods=['PUT'],
                 strict_slashes=False)
def update_reservation(reservation_id):
    """
    Updates a Reservation object.
    """
    reservation = storage.get(Reservation, reservation_id)
    if not reservation:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        setattr(reservation, k, v)
    storage.save()
    return jsonify(reservation.to_dict()), 200
