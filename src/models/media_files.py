from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, Float

from config.database import db
from src.models import User
from src.models.media_folder import MediaFolder
from src.models.mixin.TimestampMixin import TimestampMixin
from src.utils.enums import MediaAssetsType


class MediaFile(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'media_files'

    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100))
    type = db.Column(String(100))
    owner_entity_id = db.Column(Integer, nullable=True)
    folder_id = db.Column(Integer, db.ForeignKey(MediaFolder.id))
    file_location = db.Column(String(255))
    file_type = db.Column(Integer, default=MediaAssetsType.Document.value)
    file_size = db.Column(Float)
    file_name = db.Column(String(255))
    file_ext = db.Column(String(255))
    width = db.Column(Integer, nullable=True)
    height = db.Column(Integer, nullable=True)
    alt = db.Column(Text(), nullable=True)
    title = db.Column(Text(), nullable=True)
    description = db.Column(Text(), nullable=True)
    is_published = db.Column(Boolean, default=False)
    is_system_file = db.Column(Boolean, default=False)

    folder = db.relationship(MediaFolder, uselist=False)

    def __init__(self, code, type, folder_id, file_location, file_type, file_size, file_name, file_ext, is_published=None, is_system_file=None):
        if is_published is None:
            is_published = False
        if is_system_file is None:
            is_system_file = False

        self.code = code
        self.type = type
        self.folder_id = folder_id
        self.file_location = file_location
        self.file_type = file_type
        self.file_size = file_size
        self.file_name = file_name
        self.file_ext = file_ext
        self.is_published = is_published
        self.is_system_file = is_system_file

    def __repr__(self):
        return "<MediaFile(id='{}', code='{}', type='{}', folder_id='{}' file_name='{}' file_ext='{}' file_location='{}' is_published={} is_system_file={} " \
               "created_at='{}' updated_at='{}'>".format(
            self.id,
            self.code,
            self.type,
            self.folder_id,
            self.file_name,
            self.file_ext,
            self.file_location,
            self.is_published,
            self.is_system_file,
            self.created_at,
            self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
