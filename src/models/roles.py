from sqlalchemy import Integer, String, Boolean

from config.database import db


class Roles(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'roles'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    is_active = db.Column(Boolean, nullable=False)
    # Define the relationship to Role via UserRoles
    user = db.relationship('User', secondary='user_roles')

    def __init__(self, name, is_active):
        self.name = name
        self.is_active = is_active

    def __repr__(self):
        return "<Role(id='{id}', name='{name} , is_active={is_active}')>".format(id=self.id, name=self.name,
                                                                                 is_active=self.is_active)
