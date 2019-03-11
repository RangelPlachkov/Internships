"""empty message

Revision ID: b7693f626fea
Revises: cea18f2c1990
Create Date: 2019-02-28 23:24:27.660494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7693f626fea'
down_revision = 'cea18f2c1990'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_username', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    # ### end Alembic commands ###
