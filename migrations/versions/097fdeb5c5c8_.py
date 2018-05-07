"""empty message

Revision ID: 097fdeb5c5c8
Revises: 76372e726548
Create Date: 2018-05-06 19:50:39.767560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '097fdeb5c5c8'
down_revision = '76372e726548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'title')
    # ### end Alembic commands ###