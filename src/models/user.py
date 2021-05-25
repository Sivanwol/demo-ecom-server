from datetime import datetime

from sqlalchemy import Integer, String, Boolean

from config.database import db


class User(db.Model):
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
    is_pass_tutorial = db.Column(Boolean, nullable=False, default=False)
    country = db.Column(String(3), nullable=True)
    currency = db.Column(String(3), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Roles', secondary='user_roles')

    def __init__(self, uid, is_active, is_pass_tutorial, country=None, currency=None, avatar_id=0, phone='', address1='', address2=''):
        self.uid = uid
        self.avatar_id = avatar_id
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.is_active = is_active
        self.is_pass_tutorial = is_pass_tutorial
        self.country = country
        self.currency = currency

    def __repr__(self):
        return "<User(id='{id}', uid='{uid}', is_active='{is_active}' is_pass_tutorial={is_pass_tutorial})>".format(id=self.id, uid=self.uid,
                                                                                                                    is_active=self.is_active,
                                                                                                                    is_pass_tutorial=self.is_pass_tutorial)
