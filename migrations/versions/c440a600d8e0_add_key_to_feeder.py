"""add key to feeder

Revision ID: c440a600d8e0
Revises: 05db1cb87b8d
Create Date: 2019-07-31 16:42:39.577586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c440a600d8e0'
down_revision = '05db1cb87b8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feeder', sa.Column('secret_key', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feeder', 'secret_key')
    # ### end Alembic commands ###