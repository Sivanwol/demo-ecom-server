from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.models import User
from marshmallow_sqlalchemy.fields import Nested

from src.schemas.role_schema import RoleSchema


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = auto_field()
    uid = auto_field()
    address1 = auto_field()
    address2 = auto_field()
    phone = auto_field()
    is_pass_tutorial = auto_field()
    country = auto_field()
    currency = auto_field()
    roles = Nested(RoleSchema, many=True, exclude=('user',))


class FirebaseUserSchema(Schema):
    display_name = fields.String()
    disabled = fields.Boolean()
