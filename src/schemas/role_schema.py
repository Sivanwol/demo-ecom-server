from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.models import Roles


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = Roles
        include_fk = True
        load_instance = True
    id = auto_field()
    name = auto_field()
    is_active = auto_field()
    user = auto_field()
