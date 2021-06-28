import os

from marshmallow import Schema, fields, validate

from config import settings


class RequestMediaCreateFolderSchema(Schema):
    parent_folder_code = fields.UUID(missing=None, allow_none=True)
    entity_id = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=16, max=255, error='field entity_id not valid'))
    alias = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=3, max=255, error='field alias not valid'))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=255, error='field name not valid'))
    description = fields.Str(missing=None, allow_none=True)
    parent_level = fields.Integer(required=True, validate=validate.Range(min=1, max=int(settings[os.environ.get("FLASK_ENV", "development")].MAX_PARENT_LEVEL),
                                                                         error='field parent_level not valid'))
    entity_code = fields.Str(required=True, validate=validate.Length(max=100, error='field entity_code not valid'))
    is_system_folder = fields.Bool(required=True)
    is_store_folder = fields.Bool(required=True)


class RequestMediaCreateFile(Schema):
    folder_code = fields.UUID(missing=None, allow_none=True)
    alias = fields.Str(missing=None, allow_none=True, validate=validate.Length(min=3, max=255, error='field alias not valid'))
    width = fields.Integer(missing=None, allow_none=True)
    height = fields.Integer(missing=None, allow_none=True)
    alt = fields.Str(missing=None, allow_none=True)
    title = fields.Str(missing=None, allow_none=True)
    is_system_file = fields.Bool(required=True)
    is_store_file = fields.Bool(required=True)
