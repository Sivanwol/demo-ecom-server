from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.models import MediaFolder


class MediaFolderSchema(SQLAlchemySchema):
    class Meta:
        model = MediaFolder
        include_fk = True
        load_instance = True
    code = auto_field()
    alias = auto_field()
    name = auto_field()
    description = auto_field()
    is_system_folder = auto_field()
    is_store_folder = auto_field()
    owner_user_uid = auto_field()
    parent_folder_code = auto_field()
    parent_level = auto_field()
