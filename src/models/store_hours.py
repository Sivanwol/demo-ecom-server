from datetime import datetime

from sqlalchemy import Integer, String, Boolean

from config.database import db
from src.models import User


class Store(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'stores'

    id = db.Column(Integer, primary_key=True)
    store_code = db.Column(String(100), nullable=False)
    owner_id = db.Column(Integer, db.ForeignKey(User.id))
    logo_id = db.Column(Integer, nullable=True)
    name = db.Column(String(100), nullable=False)
    description = db.Column(String(255), nullable=True)
    default_currency_code = db.Column(String(3), nullable=False)
    is_maintenance = db.Column(Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    owner = db.relationship(User, uselist=False)

    def __init__(self, store_code, owner_id, name, default_currency_code, logo_id=None, description=None, is_maintenance=False):
        self.store_code = store_code
        self.owner_id = owner_id
        self.name = name
        self.default_currency_code = default_currency_code
        self.logo_id = logo_id
        self.description = description
        self.is_maintenance = is_maintenance

    def __repr__(self):
        return "<Store(id='{}', owner_id='{}', name='{}' is_maintenance={} created_at='{}' updated_at='{}'>".format(self.id,
                                                                                                                    self.owner_id,
                                                                                                                    self.name,
                                                                                                                    self.is_maintenance,
                                                                                                                    self.created_at,
                                                                                                                    self.updated_at)

    def update_hours(self, hours):
        pass

    def update_locations(self, locations):
        pass

    def remove_locations(self, location_ids):
        pass
