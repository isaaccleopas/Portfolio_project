from datetime import datetime
from models.engine.db_storage import DBStorage
from models.user import User
from models.event import Event
from models.review import Review
from models.reservation import Reservation

def populate_database():
    # Initialize the database storage
    storage = DBStorage()
    storage.reload()  # Initialize the session

    # Create some example users
    user1 = User(name="John Doe", email="john@example.com", password="password1")
    user2 = User(name="Jane Smith", email="jane@example.com", password="password2")

    # Create some example events
    event1 = Event(title="Event 1", description="Description of Event 1", image="event1.jpg",
                   venue="Venue 1", date_time=datetime(2023, 5, 26, 10, 0), slots_available=50,
                   user=user1)
    event2 = Event(title="Event 2", description="Description of Event 2", image="event2.jpg",
                   venue="Venue 2", date_time=datetime(2023, 5, 27, 15, 30), slots_available=30,
                   user=user2)

    # Create some example reviews
    review1 = Review(content="Review 1 content", event=event1, user=user1)
    review2 = Review(content="Review 2 content", event=event2, user=user2)

    # Create some example reservations
    reservation1 = Reservation(event=event1, user=user1, slots_reserved=2)
    reservation2 = Reservation(event=event2, user=user2, slots_reserved=3)

    # Add the objects to the session
    storage.new(user1)
    storage.new(user2)
    storage.new(event1)
    storage.new(event2)
    storage.new(review1)
    storage.new(review2)
    storage.new(reservation1)
    storage.new(reservation2)

    # Save the changes to the database
    storage.save()

    # Close the session
    storage.close()

if __name__ == "__main__":
    populate_database()
