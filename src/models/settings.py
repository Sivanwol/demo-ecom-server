import json

from sqlalchemy import String, Boolean, Text

from config.database import db


class Settings(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'roles'

    key = db.Column(String(255), primary_key=True)
    environment = db.Column(String(50), primary_key=True)
    description = db.Column(Text(), nullable=True)
    is_json = db.Column(Boolean, nullable=False, default=False)
    value = db.Column(Text(), nullable=True)

    def __init__(self, key, environment, description=None, is_json=False, value=None):
        self.key = key
        self.environment = environment
        self.description = description
        self.is_json = is_json
        self.value = value

    def __repr__(self):
        return "<Settings(key='{}', environment='{}' , is_json='{}' value='{})>".format(self.key, self.environment, self.is_json, self.value)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_value(self):
        if self.is_json:
            return json.loads(self.value)
        return self.value