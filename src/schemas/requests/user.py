from marshmallow import fields, Schema, validate


class CreatePlatformUser(Schema):
    role_names: fields.List(
        fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    )


class CreateStoreStaffUser(Schema):
    role: fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    email: fields.Email(required=True)
    fullname: fields.Str(required=True, validate=validate.Length(min=5, max=255, error='field name not valid'))
    password: fields.Str(required=True, validate=validate.Length(min=8, max=100, error='field name not valid'))


class UpdateUserInfo(Schema):
    fullname: fields.Str(required=True, validate=validate.Length(min=5, max=255, error='field fullname not valid'))
    phone: fields.Str(missing=True, allow_none=True,validate=validate.Length(min=5, max=100, error='field phone not valid'))
    address1: fields.Str(missing=True, allow_none=True, validate=validate.Length(min=5, max=100, error='field address1 not valid'))
    address2: fields.Str(missing=True, allow_none=True, validate=validate.Length(min=5, max=100, error='field address3 not valid'))
    country: fields.Str(missing=True, allow_none=True, validate=validate.Length(min=2, max=3, error='field country not valid'))
    currency: fields.Str(missing=True, allow_none=True, validate=validate.Length(min=2, max=3, error='field currency not valid'))