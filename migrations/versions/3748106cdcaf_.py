"""empty message

Revision ID: 3748106cdcaf
Revises: f6520373ddc2
Create Date: 2021-04-21 16:29:12.860801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3748106cdcaf'
down_revision = 'f6520373ddc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('company_url', sa.String(length=120), nullable=True))
    op.add_column('store', sa.Column('store_address', sa.String(length=120), nullable=True))
    op.add_column('store', sa.Column('store_phone', sa.String(length=15), nullable=True))
    op.add_column('store', sa.Column('store_plan', sa.String(length=64), nullable=True))
    op.add_column('store', sa.Column('store_url', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store', 'store_url')
    op.drop_column('store', 'store_plan')
    op.drop_column('store', 'store_phone')
    op.drop_column('store', 'store_address')
    op.drop_column('company', 'company_url')
    # ### end Alembic commands ###