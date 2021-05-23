from config.database import db
from src.models import Roles
from sqlalchemy.sql import or_


class RolesService:

    def get_roles(self, roles_names=None):
        if roles_names is None:
            roles_names = []
        return Roles.query.filter(or_(Roles.name == role_name for role_name in roles_names)).all()

    def check_roles(self, roles_names=None):
        if roles_names is None:
            roles_names = []
        roles = Roles.query.filter(or_(Roles.name == role_name for role_name in roles_names))
        if roles.count() == 0 or roles.count() != len(roles_names):
            return False
        return True
