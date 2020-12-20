"""empty message

Revision ID: 4203a0495a6e
Revises: e007b3312af2
Create Date: 2020-12-20 11:03:29.553221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4203a0495a6e'
down_revision = 'e007b3312af2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('producto', sa.Column('accion_cambiar_por', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('producto', 'accion_cambiar_por')
    # ### end Alembic commands ###
