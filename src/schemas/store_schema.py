from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from src.models.stores import Store
from src.schemas.user_schema import UserSchema


class StoreSchema(SQLAlchemySchema):
    class Meta:
        model = Store
        include_fk = True
        load_instance = True
    store_code = auto_field()
    owner = Nested(UserSchema)
    logo_id = auto_field()
    name = auto_field()
    description = auto_field()
    default_currency_code = auto_field()
    is_maintenance = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
