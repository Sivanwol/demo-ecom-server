from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.models import MediaFolder, MediaFile


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
    entity_code = auto_field()
    parent_folder_code = auto_field()
    parent_level = auto_field()
    created_at = auto_field()
    updated_at = auto_field()


class MediaFileSchema(SQLAlchemySchema):
    class Meta:
        model = MediaFile
        include_fk = True
        load_instance = True

    code = auto_field()
    # alias = auto_field()
    owner_user_uid = auto_field()
    entity_code = auto_field()
    folder_code = auto_field()
    file_type = auto_field()
    file_size = auto_field()
    download_uri = auto_field()
    width = auto_field()
    height = auto_field()
    alt = auto_field()
    title = auto_field()
    is_published = auto_field()
    is_system_file = auto_field()
    is_store_file = auto_field()
    updated_at = auto_field()
    created_at = auto_field()

