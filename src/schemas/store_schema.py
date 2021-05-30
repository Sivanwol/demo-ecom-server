from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from src.models.store_hours import StoreHours
from src.models.store_locations import StoreLocations
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


class StoreLocationSchema(SQLAlchemySchema):
    class Meta:
        model = StoreLocations
        include_fk = True
        load_instance = True

    lat = auto_field()
    lng = auto_field()
    store = Nested(StoreSchema)
    address = auto_field()
    city = auto_field()
    country_code = auto_field()
    is_close = auto_field()


class StoreHourSchema(SQLAlchemySchema):
    class Meta:
        model = StoreHours
        include_fk = True
        load_instance = True

    store = Nested(StoreSchema)
    location = Nested(StoreLocationSchema)
    day = auto_field()
    from_time = auto_field()
    to_time = auto_field()
    is_open_24 = auto_field()
    is_close = auto_field()


class ResponseStoreData(Schema):
    store: StoreSchema()
    store_locations: StoreLocationSchema()
