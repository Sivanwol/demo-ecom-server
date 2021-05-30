from marshmallow import Schema, fields, validate


class RequestStoreCreate(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    description = fields.Str(required=False, validate=validate.Length(max=255, error='field description not valid'))
    currency_code = fields.Str(required=True, validate=validate.Length(min=2, max=3, error='field currency_code noy valid'))


class RequestStoreUpdate(RequestStoreCreate):
    pass


class RequestStoreLocationSchema(Schema):
    lat = fields.Int(missing=None, allow_none=True)
    lng = fields.Int(missing=None, allow_none=True)
    address = fields.Str(required=True, validate=validate.Length(max=255, error='field address not valid'))
    city = fields.Str(required=True, validate=validate.Length(max=255, error='field city not valid'))
    country_code = fields.Str(required=True, validate=validate.Length(min=2, max=3, error='field country_code not valid'))
    is_close = fields.Bool(required=True)

    '''
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('store_id', sa.Integer(), sa.ForeignKey('stores.id')),
                    sa.Column('store_location_id', sa.Integer(), sa.ForeignKey('stores_locations.id')),
                    sa.Column('day', sa.Integer(), index=True, nullable=True),
                    sa.Column('from_time', sa.String(length=255), nullable=True),
                    sa.Column('to_time', sa.String(length=3), nullable=False),
                    sa.Column('is_open_24', sa.String(length=100), nullable=True),
                    sa.Column('is_close', sa.Boolean(), nullable=False, default=False),
                    '''


class RequestStoreHourSchema(Schema):
    location = fields.Nested(RequestStoreLocationSchema(),missing=None, allow_none=True)
    day = fields.Int(required=True, validate=validate.Length(max=7 , min=1, error='field day not valid'))
    from_time = fields.Str(required=True, validate=validate.Length(max=255, error='field from_time not valid'))
    to_time = fields.Str(required=True, validate=validate.Length(max=255, error='field to_time not valid'))
    is_open_24 = fields.Bool(required=True)
    is_close = fields.Bool(required=True)

class RequestStoreLocationsUpdate(Schema):
    locations = fields.Nested(RequestStoreLocationSchema())


class RequestStoreHoursUpdate(Schema):
    hours = fields.Nested(RequestStoreHourSchema())
