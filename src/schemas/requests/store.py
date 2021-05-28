from marshmallow import Schema, fields, validate


class RequestStoreCreate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    description = fields.String(required=False, validate=validate.Length(max=255, error='field description not valid'))
    currency_code = fields.String(required=True, validate=validate.Length(min=2, max=3, error='field currency_code noy valid'))


class RequestStoreUpdate(Schema):
    store_code = fields.String(required=True, dump_only=True, validate=validate.Length(min=10, max=100, error='field store_code not valid'))
    name = fields.String(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    description = fields.String(required=False, validate=validate.Length(max=255, error='field description not valid'))
    currency_code = fields.String(required=True, validate=validate.Length(min=2, max=3, error='field currency_code noy valid'))
