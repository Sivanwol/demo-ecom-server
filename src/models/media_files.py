from sqlalchemy import Integer, String, Boolean, Text, Float
from config.database import db
from src.models.media_folder import MediaFolder
from src.models.mixin import TimestampMixin
from src.utils.enums import MediaAssetsType


class MediaFile(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'media_files'

    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100))
    owner_user_uid = db.Column(String(100), db.ForeignKey('users.uid'))
    entity_id = db.Column(Integer, nullable=True)
    folder_code = db.Column(String(100), db.ForeignKey(MediaFolder.code))
    file_location = db.Column(String(255))
    file_type = db.Column(Integer, default=MediaAssetsType.Document.value)
    file_size = db.Column(Float)
    file_name = db.Column(String(255))
    width = db.Column(Integer, nullable=True)
    height = db.Column(Integer, nullable=True)
    alt = db.Column(Text(), nullable=True)
    title = db.Column(Text(), nullable=True)
    is_published = db.Column(Boolean, default=False)
    is_system_file = db.Column(Boolean, default=False)
    is_store_file = db.Column(Boolean, nullable=False)

    folder = db.relationship(MediaFolder, uselist=False)
    owner = db.relationship("User", foreign_keys=[owner_user_uid])

    def __init__(self, code, owner_uid,  folder_code, file_location, file_type, file_size, file_name, file_ext, is_published=None, is_system_file=None,
                 is_store_file=None):
        if is_published is None:
            is_published = False
        if is_system_file is None:
            is_system_file = False
        if is_store_file is None:
            is_store_file = False

        self.code = code
        self.owner_user_uid = owner_uid
        self.folder_code = folder_code
        self.file_location = file_location
        self.file_type = file_type
        self.file_size = file_size
        self.file_name = file_name
        self.file_ext = file_ext
        self.is_published = is_published
        self.is_system_file = is_system_file
        self.is_store_file = is_store_file

    def __repr__(self):
        return "<MediaFile(id='{}', code='{}', owner_user_uid='{}', folder_code='{}' file_name='{}' file_ext='{}' file_location='{}' " \
               "is_published={} is_store_file={} is_system_file={} created_at='{}' updated_at='{}'>".format(
            self.id,
            self.code,
            self.owner_user_uid,
            self.folder_code,
            self.file_name,
            self.file_ext,
            self.file_location,
            self.is_published,
            self.is_store_file,
            self.is_system_file,
            self.created_at,
            self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
