from marshmallow import Schema, fields, validate


class UserRolesList(Schema):
    role_names: fields.List(
        fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    )


class CreateStoreStaffUser(Schema):
    roles = fields.List(
        fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field role not valid'))
    )
    email = fields.Email(required=True)
    fullname = fields.Str(required=True, validate=validate.Length(min=5, max=255, error='field name not valid'))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=100, error='field name not valid'))


class UpdateUserInfo(Schema):
    fullname = fields.Str(required=True, validate=validate.Length(min=5, max=255, error='field fullname not valid'))
    address1 = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=5, max=100, error='field address1 not valid'))
    address2 = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=5, max=100, error='field address3 not valid'))
    country = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=2, max=3, error='field country not valid'))
    currency = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=2, max=3, error='field currency not valid'))
