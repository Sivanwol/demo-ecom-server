"""add media table

Revision ID: 29be447fbfe5
Revises: aace8b1bfe38
Create Date: 2021-06-20 16:48:49.148007

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.

revision = '29be447fbfe5'
down_revision = 'aace8b1bfe38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_media_assets_file_name', table_name='media_assets')
    op.drop_table('media_assets')

    op.create_table('media_folders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(length=100), index=True, nullable=False, unique=True),
                    sa.Column('owner_user_uid', sa.String(length=100), sa.ForeignKey('users.uid')),
                    sa.Column('entity_code', sa.String(length=100), index=True),
                    sa.Column('parent_folder_code', sa.Integer(), sa.ForeignKey('media_folders.code'), index=True, nullable=True),
                    sa.Column('parent_level', sa.Integer(), nullable=False, default=1),
                    sa.Column('alias', sa.String(length=255), index=True, nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('is_system_folder', sa.Boolean(), nullable=True, default=False),
                    sa.Column('is_store_folder', sa.Boolean(), nullable=True, default=False),
                    sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
                    sa.Column('updated_at', sa.DateTime(), onupdate=sa.ColumnDefault(sa.func.current_timestamp), default=sa.func.current_timestamp()),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('media_files',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(length=255), index=True, nullable=False, unique=True),
                    sa.Column('owner_user_uid', sa.String(length=100), sa.ForeignKey('users.uid')),
                    sa.Column('entity_code', sa.String(length=100), index=True),
                    sa.Column('folder_code', sa.String(length=100), sa.ForeignKey('media_folders.code'), index=True, nullable=True),
                    sa.Column('alias', sa.String(length=255), index=True, nullable=True),
                    sa.Column('file_location', sa.String(length=255), nullable=False),
                    sa.Column('file_type', sa.Integer(), nullable=False, default=3),
                    sa.Column('file_size', sa.Float(), nullable=False),
                    sa.Column('file_name', sa.String(length=255), nullable=False),
                    sa.Column('width', sa.Integer(), nullable=True),
                    sa.Column('height', sa.Integer(), nullable=True),
                    sa.Column('alt', sa.Text(), nullable=True),
                    sa.Column('title', sa.Text(), nullable=True),
                    sa.Column('is_published', sa.Boolean(), default=False),
                    sa.Column('is_system_file', sa.Boolean(), default=False),
                    sa.Column('is_store_file', sa.Boolean(), nullable=True, default=False),
                    sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
                    sa.Column('updated_at', sa.DateTime(), onupdate=sa.ColumnDefault(sa.func.current_timestamp), default=sa.func.current_timestamp()),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.alter_column("users", "avatar_code", sa.ForeignKey('media_files.code'), modify_type=sa.String(length=100))
    op.alter_column("stores", "logo_code", sa.ForeignKey('media_files.code'), modify_type=sa.String(length=100), nullable=True, index=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", 'avatar_id', sa.Integer(), nullable=True)
    op.alter_column("stores", "logo_id", sa.Integer(), nullable=True)
    op.drop_table('media_files')
    op.drop_table('media_folders')
    op.create_table('media_assets',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
                    sa.Column('alt', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
                    sa.Column('file_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
                    sa.Column('path', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
                    sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('width', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='media_assets_pkey')
                    )
    op.create_index('ix_media_assets_file_name', 'media_assets', ['file_name'], unique=False)
    # ### end Alembic commands ###
