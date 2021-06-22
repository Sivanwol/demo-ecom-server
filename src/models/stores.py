from sqlalchemy import Integer, String, Boolean

from config.database import db
from src.models.user import User
from src.models.media_files import MediaFile
from src.models.mixin import TimestampMixin


class Store(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'stores'

    id = db.Column(Integer, primary_key=True)
    store_code = db.Column(String(100), nullable=False)
    owner_user_uid = db.Column(String(100), db.ForeignKey('users.uid'))
    logo_id = db.Column(Integer, db.ForeignKey(MediaFile.id), nullable=True)
    name = db.Column(String(100), nullable=False)
    description = db.Column(String(255), nullable=True)
    default_currency_code = db.Column(String(3), nullable=False)
    # Note only owner able set this on or off
    is_maintenance = db.Column(Boolean, nullable=False, default=False)

    logo = db.relationship(MediaFile, uselist=False)
    owner = db.relationship("User", foreign_keys=[owner_user_uid])

    def __init__(self, store_code, owner_uid, name, default_currency_code, logo_id=None, description=None, is_maintenance=False):
        self.store_code = store_code
        self.owner_user_uid = owner_uid
        self.name = name
        self.default_currency_code = default_currency_code
        self.logo_id = logo_id
        self.description = description
        self.is_maintenance = is_maintenance

    def __repr__(self):
        return "<Store(id='{}', owner_id='{}', name='{}' is_maintenance={} created_at='{}' updated_at='{}'>".format(self.id,
                                                                                                                    self.owner_user_uid,
                                                                                                                    self.name,
                                                                                                                    self.is_maintenance,
                                                                                                                    self.created_at,
                                                                                                                    self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update_hours(self, hours):
        pass

    def update_locations(self, locations):
        pass

    def remove_locations(self, location_ids):
        pass
