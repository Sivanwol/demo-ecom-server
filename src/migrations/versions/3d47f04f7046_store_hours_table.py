"""store hours table

Revision ID: 3d47f04f7046
Revises: 786cc7ba97f6
Create Date: 2021-05-25 09:30:42.835868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d47f04f7046'
down_revision = '786cc7ba97f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores_hours',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('store_id', sa.Integer(), sa.ForeignKey('stores.id')),
                    sa.Column('store_location_id', sa.Integer(), sa.ForeignKey('stores_locations.id')),
                    sa.Column('day', sa.Integer(), nullable=True),
                    sa.Column('from_time', sa.String(length=255), nullable=True),
                    sa.Column('to_time', sa.String(length=3), nullable=False),
                    sa.Column('is_open_24', sa.String(length=100), nullable=True),
                    sa.Column('is_close', sa.Boolean(), nullable=False, default=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('stores_hours_owner_id_fkey', 'stores_hours', type_='foreignkey')
    op.drop_constraint('stores_hours_store_location_id_fkey', 'stores_hours', type_='foreignkey')
    op.drop_table('stores')
    # ### end Alembic commands ###
