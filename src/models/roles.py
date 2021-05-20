from flask_security import RoleMixin
from sqlalchemy import Integer, String, Boolean

from config.database import db


class Roles(db.Model, RoleMixin):
    """
    This is a base user Model
    """
    __tablename__ = 'roles'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    is_active = db.Column(Boolean, nullable=False)

    def __init__(self, name, is_active):
        self.name = name
        self.is_active = is_active

    def __repr__(self):
        return "<Role(id='{id}', name='{name} , is_active={is_active}')>".format(id=self.id, name=self.name,
                                                                                 is_active=self.is_active)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
