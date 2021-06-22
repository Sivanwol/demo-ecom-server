from sqlalchemy import Integer,  Boolean
from config.database import db
from src.models.store_locations import StoreLocations
from src.models.stores import Store


class StoreHours(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'stores_hours'

    id = db.Column(Integer, primary_key=True)
    store_id = db.Column(Integer, db.ForeignKey(Store.id))
    store_location_id = db.Column(Integer, db.ForeignKey(StoreLocations.id))
    day = db.Column(Integer, nullable=False)
    from_time = db.Column(Integer, nullable=True)
    to_time = db.Column(Integer, nullable=True)
    is_open_24 = db.Column(Boolean, nullable=False, default=False)
    is_close = db.Column(Boolean, nullable=False, default=False)

    store = db.relationship(Store, uselist=False)
    location = db.relationship(StoreLocations, uselist=False)


    def __init__(self, store_id, day, store_location_id=None, from_time=None, to_time=None, is_open_24=False, is_close=False):
        self.store_id = store_id
        self.day = day
        self.store_location_id = store_location_id
        self.from_time = from_time
        self.to_time = to_time
        self.is_open_24 = is_open_24
        self.is_close = is_close

    def __repr__(self):
        return "<Store_Hours(id='{}', store_id='{}', day='{}' store_location_id={} from_time='{}' to_time='{}' is_open_24='{}' is_close='{}'>".format(
            self.id,
            self.store_id,
            self.day,
            self.store_location_id,
            self.from_time,
            self.to_time,
            self.is_open_24,
            self.is_close)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
