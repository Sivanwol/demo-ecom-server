from config.database import db


class UserRoles(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "<User_Role(user_id='{}', role_id='{}')>".format(self.user_id, self.role_id)

