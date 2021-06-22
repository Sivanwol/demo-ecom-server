from sqlalchemy import Integer, String, Boolean

from config.database import db
from src.models.media_files import MediaFile
from src.models.mixin import TimestampMixin


class User(TimestampMixin, db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    uid = db.Column(String(100), nullable=False)
    avatar_id = db.Column(Integer, db.ForeignKey(MediaFile.id), nullable=True)
    email = db.Column(String(100), nullable=False, unique=True, index=True)
    phone = db.Column(String(100), nullable=True)
    store_code = db.Column(String(100), nullable=True, index=True)
    fullname = db.Column(String(255), nullable=False, index=True)
    address1 = db.Column(String(255), nullable=True)
    address2 = db.Column(String(255), nullable=True)
    is_active = db.Column(Boolean, nullable=False, default=False)
    is_pass_tutorial = db.Column(Boolean, nullable=False, default=False)
    country = db.Column(String(3), nullable=True)
    currency = db.Column(String(3), nullable=True)

    # Define the relationships
    roles = db.relationship('Roles', secondary='user_roles')
    avatar = db.relationship(MediaFile, uselist=False, foreign_keys=[avatar_id])

    def __init__(self, uid, email, fullname, is_active, is_pass_tutorial, country=None, currency=None, store_code=None, avatar_id=0, phone='', address1='',
                 address2=''):
        self.uid = uid
        self.fullname = fullname
        self.avatar_id = avatar_id
        self.email = email
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.is_active = is_active
        self.is_pass_tutorial = is_pass_tutorial
        self.country = country
        self.currency = currency
        self.store_code = store_code

    def __repr__(self):
        return "<User(id='{id}', uid='{uid}', email='{email}', fullname='{fullname}', is_active='{is_active}' is_pass_tutorial={is_pass_tutorial} store_code='{store_code})>".format(
            id=self.id,
            uid=self.uid,
            fullname=self.fullname,
            is_active=self.is_active,
            is_pass_tutorial=self.is_pass_tutorial,
            email=self.email,
            store_code=self.store_code)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def has_any_role(self, roles):
        match_roles = 0
        for role in roles:
            for user_role in self.roles:
                if role == user_role.name:
                    match_roles = 1 + match_roles
        return match_roles != 0

    def has_role(self, roles):
        match_roles = 0
        for role in roles:
            for user_role in self.roles:
                if role == user_role.name:
                    match_roles = 1 + match_roles
        return match_roles == len(roles)

    def add_user_roles(self, roles):
        for role in roles:
            self.roles.append(role)

    def remove_user_roles(self, roles):
        for role in roles:
            for user_role in self.roles:
                self.roles.filter(lambda user_role: role != user_role.name)
