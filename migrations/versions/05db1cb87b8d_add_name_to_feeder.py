"""add name to feeder

Revision ID: 05db1cb87b8d
Revises: 3e0d55e70670
Create Date: 2019-07-10 16:38:09.250959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05db1cb87b8d'
down_revision = '3e0d55e70670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feeder', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feeder', 'name')
    # ### end Alembic commands ###
