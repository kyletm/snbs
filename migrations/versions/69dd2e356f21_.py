"""empty message

Revision ID: 69dd2e356f21
Revises: 789913dccc9e
Create Date: 2018-05-06 22:53:42.012924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69dd2e356f21'
down_revision = '789913dccc9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('institution', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'institution')
    # ### end Alembic commands ###
