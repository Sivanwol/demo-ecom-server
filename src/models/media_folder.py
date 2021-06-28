from sqlalchemy import Integer, String, Boolean, Text, asc, desc

from config.database import db
from src.models.mixin import TimestampMixin


class MediaFolder(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'media_folders'

    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100))
    owner_user_uid = db.Column(String(100), db.ForeignKey('users.uid'))
    entity_code = db.Column(String(100), nullable=True)
    alias = db.Column(String(255), nullable=True)
    name = db.Column(String(255))
    description = db.Column(Text(), nullable=True)
    is_system_folder = db.Column(Boolean, nullable=True, default=False)
    is_store_folder = db.Column(Boolean, nullable=True, default=False)
    parent_level = db.Column(Integer, default=1)
    parent_folder_code = db.Column(String(100), nullable=True)

    owner = db.relationship("User", foreign_keys=[owner_user_uid])

    def __init__(self, code, entity_code, owner_uid, name, alias=None, description=None, is_system_folder=None, is_store_folder=None, parent_level=1,
                 parent_folder_code=None):
        if is_system_folder is None:
            is_system_folder = False
        if is_store_folder is None:
            is_store_folder = False
        self.code = code
        self.owner_user_uid = owner_uid
        self.alias = alias
        self.name = name
        self.entity_code = entity_code
        self.description = description
        self.is_system_folder = is_system_folder
        self.is_store_folder = is_store_folder
        self.parent_folder_code = parent_folder_code
        self.parent_level = parent_level

    def __repr__(self):
        return "<MediaFolder(id='{}', owner_user_uid='{}', code='{}', alias='{}',name='{}', entity_code='{}'" \
               "is_store_folder={} is_system_folder={} ,parent_folder_code={}, parent_level={}, created_at='{}', updated_at='{}'>".format(
            self.id,
            self.code,
            self.owner_user_uid,
            self.alias,
            self.name,
            self.entity_code,
            self.is_store_folder,
            self.is_system_folder,
            self.parent_folder_code,
            self.parent_level,
            self.created_at,
            self.updated_at)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_all_child_folders(self, limit_next_level=False):
        beginning_getter = db.session.query(MediaFolder). \
            filter(MediaFolder.parent_folder_code == self.code).cte(name='children_for', recursive=True)
        with_recursive = beginning_getter.union_all(
            db.session.query(MediaFolder).filter(MediaFolder.parent_folder_code == beginning_getter.c.code)
        )
        if limit_next_level:
            with_recursive = beginning_getter.union_all(
                db.session.query(MediaFolder).filter(MediaFolder.parent_folder_code == beginning_getter.c.code,
                                                     MediaFolder.parent_level == MediaFolder.parent_level + 1)
            )
        return db.session.query(with_recursive).all()
