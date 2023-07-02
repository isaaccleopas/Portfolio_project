from models.base_model import BaseModel, Base
from models.event import Event
from models.reservation import Reservation
from models.review import Review
from models.user import User
from models.engine.db_storage import DBStorage

storage = DBStorage()
Base.metadata.create_all(storage._DBStorage__engine)
storage.all(User)
