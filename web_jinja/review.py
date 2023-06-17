#!/usr/bin/python3
"""Review Functionality"""
from flask import render_template, redirect, url_for, request, flash, abort
from models.review import Review
from models.event import Event
from models.user import User

@app.route('/events/<event_id>/review', methods=['GET', 'POST'])
def review_event(event_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            user_id = get_user_id()
            user = User.query.get(user_id)
            if not user:
                abort(404)
            review = Review(content=content, event_id=event_id, user=user)
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

