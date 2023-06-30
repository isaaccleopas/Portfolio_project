#!/usr/bin/python3
"""
This module handles all default RestFul API actions for Reviews.
"""

from flask import abort, jsonify, request
from models import storage
from models.event import Event
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """
    Retrieves the list of all Review objects.
    """
    reviews = storage.all(Review).values()
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/events/<event_id>/reviews', methods=['GET'], strict_slashes=False)
def get_event_reviews(event_id):
    """
    Retrieves the list of reviews for a specific event.
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    reviews = storage.all(Review).values()
    event_reviews = [review for review in reviews if review.event_id == event_id]

    return jsonify([review.to_dict() for review in event_reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review():
    """
    Creates a new Review object.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    content = req_data.get('content')
    event_id = req_data.get('event_id')
    user_id = req_data.get('user_id')
    if not content or not event_id or not user_id:
        abort(400, "Missing required fields")
    event = storage.get(Event, event_id)
    if not event:
        abort(404)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    review = Review(content=content, event_id=event_id, user_id=user_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
