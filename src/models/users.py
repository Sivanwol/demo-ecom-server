from sqlalchemy import Integer, String, Boolean

from config.database import db


class Users(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    uid = db.Column(String(100), nullable=False)
    avatar_id = db.Column(Integer, nullable=True)
    phone = db.Column(String(100), nullable=True)
    address1 = db.Column(String(255), nullable=True)
    address2 = db.Column(String(255), nullable=True)
    is_active = db.Column(Boolean, nullable=False, default=False)

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Roles', secondary='user_roles')

    def __init__(self, uid, is_active, avatar_id=0, phone='', address1='', address2=''):
        self.uid = uid
        self.avatar_id = avatar_id
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.is_active = is_active

    def __repr__(self):
        return "<User(id='{id}', uid='{uid}', is_active='{is_active}')>".format(id=self.id, uid=self.uid, is_active=self.is_active)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
