#!/usr/bin/python3
import os
#Print environment variables
print(os.environ.get('EVENT_MYSQL_HOST'))
print(os.environ.get('EVENT_MYSQL_USER'))
print(os.environ.get('EVENT_MYSQL_PASSWORD'))
print(os.environ.get('EVENT_MYSQL_DB'))
print(os.environ.get('EVENT_TYPE_STORAGE'))

from models import storage
from models.user import User
from models.event import Event
from models.review import Review
from models.reservation import Reservation

# Set environment variable
os.environ['EVENT_MYSQL_HOST'] = 'localhost'
os.environ['EVENT_MYSQL_USER'] = 'event_dev'
os.environ['EVENT_MYSQL_PWD'] = 'Event_dev_pwd1@'
os.environ['EVENT_MYSQL_DB'] = 'event_dev_db'


# Create user instance
user = User(name="John Doe", email="johndoe@example.com", password="password123")
user.save()

# Create event instance
event = Event(title="Event 1", description="Description of Event 1", image="event1.jpg", venue="Venue 1")
event.save()

# Create review instance
review = Review(content="This event was great!", event_id=event.id, user_id=user.id)
review.save()

# Create reservation instance
reservation = Reservation(event_id=event.id)
reservation.save()

# Access the populated data
all_users = storage.all(User)
all_events = storage.all(Event)
all_reviews = storage.all(Review)
all_reservations = storage.all(Reservation)

# Print the populated data
for user in all_users.values():
    print(user)

for event in all_events.values():
    print(event)

for review in all_reviews.values():
    print(review)

for reservation in all_reservations.values():
    print(reservation)
