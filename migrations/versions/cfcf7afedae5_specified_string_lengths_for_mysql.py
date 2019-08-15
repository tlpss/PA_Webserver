"""specified string lengths for MySQL

Revision ID: cfcf7afedae5
Revises: c440a600d8e0
Create Date: 2019-08-15 10:57:32.045984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfcf7afedae5'
down_revision = 'c440a600d8e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feeder', sa.Column('desc', sa.String(length=240), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feeder', 'desc')
    # ### end Alembic commands ###