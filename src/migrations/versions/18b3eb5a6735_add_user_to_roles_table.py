"""add user to roles table

Revision ID: 18b3eb5a6735
Revises: cdd7027488fd
Create Date: 2021-05-19 21:09:12.445404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18b3eb5a6735'
down_revision = 'cdd7027488fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
             sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
             sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id')))
    # ### end Alembic commands ###


def downgrade():
    op.drop_constraint('user_roles_user_id_fkey', 'user_roles', type_='foreignkey')
    op.drop_constraint('user_roles_role_id_fkey', 'user_roles', type_='foreignkey')
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    # ### end Alembic commands ###
