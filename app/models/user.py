from sqlalchemy import Integer, String, Boolean

from app import db


class User(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    uid = db.Column(String(100), nullable=False)
    is_admin = db.Column(Boolean, nullable=False , default=False)

    def __init__(self, uid, is_admin):
        self.uid = uid
        self.is_admin = is_admin

    def __repr__(self):
        return "<User(uid='{uid}', is_admin='{is_admin}')>".format (uid=self.uid, is_admin=self.is_admin)
