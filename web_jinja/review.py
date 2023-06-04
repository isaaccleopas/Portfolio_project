#!/usr/bin/python3
"""Review Functionality"""
from flask import render_template, redirect, url_for
from models.review import Review
from models.event import Event

@app.route('/events/<event_id>/review', methods=['GET', 'POST'])
def review_event(event_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            review = Review(content=content, event_id=event_id, user_id=user_id)
            storage.new(review)
            storage.save()
            flash('Review submitted successfully!')
            return redirect(url_for('event_details', event_id=event_id))
        else:
            flash('Please enter a review before submitting.')

    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    return render_template('review.html', event=event)
