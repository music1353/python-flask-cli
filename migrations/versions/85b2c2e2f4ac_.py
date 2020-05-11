"""empty message

Revision ID: 85b2c2e2f4ac
Revises: de3544c96039
Create Date: 2020-05-11 17:21:55.740832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85b2c2e2f4ac'
down_revision = 'de3544c96039'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('uid', sa.Integer(), nullable=False))
    op.drop_constraint('users_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'auths', ['uid'], ['id'])
    op.drop_column('users', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_id_fkey', 'users', 'auths', ['id'], ['id'])
    op.drop_column('users', 'uid')
    # ### end Alembic commands ###
