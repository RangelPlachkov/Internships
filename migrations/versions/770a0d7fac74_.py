"""empty message

Revision ID: 770a0d7fac74
Revises: 83ec6c762bf2
Create Date: 2019-04-16 17:33:02.766803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '770a0d7fac74'
down_revision = '83ec6c762bf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Application', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Application', type_='unique')
    # ### end Alembic commands ###
