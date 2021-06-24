import os

from marshmallow import Schema, fields, validate

from config import settings


class RequestMediaCreateFolderSchema(Schema):
    parent_folder_code = fields.UUID(missing=None, allow_none=True)
    entity_id = fields.UUID(missing=None, allow_none=True)
    alias = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=3, max=255, error='field alias not valid'))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=255, error='field name not valid'))
    description = fields.Str(missing=None, allow_none=True)
    parent_level = fields.Integer(required=True, validate=validate.Range(min=1, max=int(settings[os.environ.get("FLASK_ENV", "development")].MAX_PARENT_LEVEL)
                                                                     , error='field parent_level not valid'))
    type = fields.Str(required=True, validate=validate.OneOf(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_TYPE_OPTIONS))
    is_system_folder = fields.Bool(required=True)
