"""empty message

Revision ID: 082e4d69767b
Revises: 048023a44a1b
Create Date: 2021-04-02 17:08:01.917651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082e4d69767b'
down_revision = '048023a44a1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('company_country', sa.String(length=20), nullable=True))
    op.add_column('company', sa.Column('company_main_currency', sa.String(length=20), nullable=True))
    op.add_column('company', sa.Column('company_main_language', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'company_main_language')
    op.drop_column('company', 'company_main_currency')
    op.drop_column('company', 'company_country')
    # ### end Alembic commands ###