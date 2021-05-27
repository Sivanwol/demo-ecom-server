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

        for r in roles:
            role = Roles.query.filter_by(name=r['name']).first()
            if role is None:
                role = Roles(r['name'], r['is_active'])
            # role.reset_permissions()
            # for perm in roles[r]:
            #     role.add_permission(perm)
            db.session.add(role)
        db.session.commit()
