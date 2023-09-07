"""empty message

Revision ID: 4da4fc561490
Revises: 
Create Date: 2023-04-03 10:34:45.137797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4da4fc561490'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('producto', sa.Column('observaciones', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('producto', 'observaciones')
    # ### end Alembic commands ###
