"""added login fields

Revision ID: 33280b7bab9f
Revises: 8107773587b0
Create Date: 2023-05-16 14:08:13.036482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33280b7bab9f'
down_revision = '8107773587b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('super_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_authenticated', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('is_anonymous', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('super_user', schema=None) as batch_op:
        batch_op.drop_column('is_anonymous')
        batch_op.drop_column('is_authenticated')

    # ### end Alembic commands ###
