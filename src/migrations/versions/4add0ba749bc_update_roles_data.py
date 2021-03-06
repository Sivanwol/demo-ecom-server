"""update roles data

Revision ID: 4add0ba749bc
Revises: 45985f33020b
Create Date: 2021-05-25 17:58:23.025479

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4add0ba749bc'
down_revision = '45985f33020b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    roles = sa.table('roles',
                     sa.Column('id', sa.Integer()),
                     sa.Column('name', sa.String()),
                     sa.Column('is_global', sa.Boolean()),
                     sa.Column('is_active', sa.Boolean())
                     )

    op.bulk_insert(roles, [
        {'name': 'owner', 'is_global': True, 'is_active': True},
        {'name': 'reports', 'is_global': True, 'is_active': True},
        {'name': 'accounts', 'is_global': True, 'is_active': True},
        {'name': 'store_owner', 'is_global': False, 'is_active': True},
        {'name': 'store_account', 'is_global': False, 'is_active': True},
        {'name': 'store_customer', 'is_global': False, 'is_active': True},
        {'name': 'store_reports', 'is_global': False, 'is_active': True},
        {'name': 'store_support', 'is_global': False, 'is_active': True},
        {'name': 'support', 'is_global': True, 'is_active': True},
    ])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    roles_name = ['\'owner\'', '\'reports\'', '\'accounts\'', '\'store_owner\'',
                  '\'store_account\'', '\'store_customer\'', '\'store_reports\'',
                  '\'store_support\'', '\'support\'']
    op.execute('delete from roles where name in ({})'.format(','.join(roles_name)))
    # ### end Alembic commands ###
