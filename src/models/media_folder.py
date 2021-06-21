from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text

from config.database import db
from src.models.mixin.TimestampMixin import TimestampMixin


class MediaFolder(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'media_folders'

    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100), nullable=False)
    alias = db.Column(String(255))
    name = db.Column(String(255))
    description = db.Column(Text(), nullable=True)
    is_system_folder = db.Column(Boolean, nullable=True, default=False)
    parent_folder_id = db.Column(Integer, nullable=True)

    def __init__(self, code, alias, name, description=None, is_system_folder=None, parent_folder_id=None):
        self.code = code
        self.alias = alias
        self.name = name
        self.description = description
        self.is_system_folder = is_system_folder
        self.parent_folder_id = parent_folder_id

    def __repr__(self):
        return "<MediaFolder(id='{}', code='{}', alias='{}', name='{}' is_system_folder={} parent_folder_id={} created_at='{}' updated_at='{}'>".format(
            self.id,
            self.code,
            self.alias,
            self.name,
            self.is_system_folder,
            self.parent_folder_id,
            self.created_at,
            self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

