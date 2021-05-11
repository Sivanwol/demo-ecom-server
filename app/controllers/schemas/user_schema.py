from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    uid = fields.String()
    is_admin = fields.Boolean()

class FirebaseUserSchame(Schema):
    uid = fields.String()
    disabled = fields.Boolean()
    email = fields.String()
    display_name = fields.String()
    photo_url = fields.String()
    phone_number = fields.String()
    tenant_id = fields.String()

# This schema will validate the incoming request's query string
class UserQueryStringSchema(Schema):
    pass

# This schema will marshal the outgoing response
class UserResponseSchema(Schema):
    user = fields.Nested(UserSchema, many=False)
    extend_info = fields.Nested(UserSchema, many=False)