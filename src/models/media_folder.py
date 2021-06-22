from sqlalchemy import Integer, String, Boolean, Text

from config.database import db
from src.models.mixin import TimestampWithOwnerUserMixin


class MediaFolder(TimestampWithOwnerUserMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'media_folders'

    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100))
    alias = db.Column(String(255), nullable=True)
    name = db.Column(String(255))
    description = db.Column(Text(), nullable=True)
    is_system_folder = db.Column(Boolean, nullable=True, default=False)
    parent_folder_code = db.Column(String(100), nullable=True)

    def __init__(self, code, owner_uid, name, alias=None, description=None, is_system_folder=None, parent_folder_code=None):
        self.code = code
        self.owner_user_uid = owner_uid
        self.alias = alias
        self.name = name
        self.description = description
        self.is_system_folder = is_system_folder
        self.parent_folder_code = parent_folder_code

    def __repr__(self):
        return "<MediaFolder(id='{}', owner_user_uid='{}', code='{}', alias='{}', " \
               "name='{}' is_system_folder={} parent_folder_code={} created_at='{}' updated_at='{}'>".format(
            self.id,
            self.code,
            self.owner_user_uid,
            self.alias,
            self.name,
            self.is_system_folder,
            self.parent_folder_code,
            self.created_at,
            self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
