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


class RequestStoreLocationsUpdate(Schema):
    locations = fields.Nested(RequestStoreLocationSchema())
