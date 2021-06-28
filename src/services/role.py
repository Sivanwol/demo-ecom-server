from flask import Flask

from src.models import Roles
from sqlalchemy.sql import or_


class RoleService:

    def __init__(self, app: Flask):
        self.logger = app.logger


    def get_all_roles(self):
        return Roles.query.all()

    def list_roles(self, is_store_owner=True):
        return Roles.query.filter(Roles.is_global != is_store_owner).all()

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

    def insert_roles(self):
        Roles.insert_roles()
