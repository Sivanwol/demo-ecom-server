"""setup store table

Revision ID: 786cc7ba97f6
Revises: dbad07d7ae72
Create Date: 2021-05-25 09:15:50.158569

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '786cc7ba97f6'
down_revision = 'dbad07d7ae72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('store_code', sa.String(length=100), unique=True, index=True, nullable=True),
                    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id')),
                    sa.Column('logo_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('default_currency_code', sa.String(length=3), nullable=False),
                    sa.Column('is_maintenance', sa.Boolean(), nullable=False, default=False),
                    sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
                    sa.Column('updated_at', sa.DateTime(), onupdate=sa.ColumnDefault(sa.func.current_timestamp), default=sa.func.current_timestamp()),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('stores_owner_id_fkey', 'stores', type_='foreignkey')
    op.drop_table('stores')
    # ### end Alembic commands ###
