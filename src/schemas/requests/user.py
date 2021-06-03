from marshmallow import fields, Schema, validate


class CreatePlatformUser(Schema):
    role_names: fields.List(
        fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    )


class CreateStoreStaffUser(Schema):
    role: fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    email: fields.Email(required=True)
    password: fields.Str(required=True, validate=validate.Length(min=8, max=100, error='field name not valid'))
