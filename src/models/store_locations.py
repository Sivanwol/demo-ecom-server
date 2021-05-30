from sqlalchemy import Integer, String, Boolean

from config.database import db
from src.models.stores import Store


class StoreLocations(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'stores_locations'

    id = db.Column(Integer, primary_key=True)
    store_id = db.Column(Integer, db.ForeignKey(Store.id))
    lat = db.Column(Integer, nullable=True)
    lng = db.Column(Integer, nullable=True)
    address = db.Column(String(255), nullable=False)
    city = db.Column(String(255), nullable=False)
    country_code = db.Column(String(3), nullable=False)
    is_close = db.Column(Boolean, nullable=False, default=False)

    store = db.relationship(Store, uselist=False)

    def __init__(self, store_id, address, city, country_code, lat=None, lng=None, is_close=None):
        self.store_id = store_id
        self.lat = lat
        self.lng = lng
        self.address = address
        self.city = city
        self.country_code = country_code
        self.is_close = is_close

    def __repr__(self):
        return "<Store_Location(id='{}',store_id='{}', lat='{}', lng='{}' address='{}' city='{}' country_code='{}'>".format(
            self.id,
            self.store_id,
            self.lat,
            self.lng,
            self.address,
            self.city,
            self.country_code)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}