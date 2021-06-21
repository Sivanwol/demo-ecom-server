from sqlalchemy import Integer, String, Boolean

from config.database import db


class Roles(db.Model):
    """
    This is a base user Model
    """
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    is_global = db.Column(Boolean, nullable=False, default=False)
    is_active = db.Column(Boolean, nullable=False, default=True)
    # Define the relationship to Role via UserRoles
    user = db.relationship('User', secondary='user_roles', viewonly=True)

    def __init__(self, name, is_global=False, is_active=True):
        self.name = name
        self.is_active = is_active
        self.is_global = is_global

    def __repr__(self):
        return "<Role(id='{}', name='{} , is_active={}')>".format(id, self.name, self.is_global, self.is_active)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def insert_roles():
        roles = [
            {'name': 'owner', 'is_active': True},
            {'name': 'reports', 'is_active': True},
            {'name': 'accounts', 'is_active': True},
            {'name': 'store_owner', 'is_active': True},
            {'name': 'store_account', 'is_active': True},
            {'name': 'store_customer', 'is_active': True},
            {'name': 'store_reports', 'is_active': True},
            {'name': 'store_support', 'is_active': True},
            {'name': 'support', 'is_active': True},
        ]

        for role in roles:
            role_db = Roles.query.filter_by(name=role['name']).first()
            if role_db is None:
                record = Roles(role['name'], role['is_active'])
                db.session.add(record)
            # role.reset_permissions()
            # for perm in roles[r]:
            #     role.add_permission(perm)
        db.session.commit()
