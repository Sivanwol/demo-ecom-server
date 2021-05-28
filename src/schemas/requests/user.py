from marshmallow import fields, Schema, validate


class CreatePlatformUser(Schema):
    role_names: fields.List(
        fields.String(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    )
