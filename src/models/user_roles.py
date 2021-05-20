from firebase_admin._user_mgt import UserManager

from config.api import app
from config.database import db
from src.models.users import Users


class UserRoles(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, Users)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(id='{id}', name='{name}')>".format(id=self.id, name=self.name)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
