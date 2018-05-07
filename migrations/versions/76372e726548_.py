"""empty message

Revision ID: 76372e726548
Revises: d08761007e7e
Create Date: 2018-05-06 19:45:48.431255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76372e726548'
down_revision = 'd08761007e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'price')
    # ### end Alembic commands ###