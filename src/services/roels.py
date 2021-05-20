from config.database import db
from src.models import Users, Roles
from sqlalchemy.sql import or_


class RolesService:

    def get_roles(self, roles_names=None):
        if roles_names is None:
            roles_names = []
        return Roles.query.filter(or_(Roles.name == role_name for role_name in roles_names)).all()

    def sync_user(self, uid, roles):
        user = Users(uid, True)
        db.session.add(user)
        db.session.commit()
