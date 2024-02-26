"""empty message

Revision ID: 8d1b06b52fc8
Revises: 4da4fc561490
Create Date: 2024-02-02 18:26:59.514549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d1b06b52fc8'
down_revision = '4da4fc561490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('metodo_envio_sucursal', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'metodo_envio_sucursal')
    # ### end Alembic commands ###