"""empty message

Revision ID: 65fd79bc2d10
Revises: 
Create Date: 2022-03-24 17:51:16.130649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65fd79bc2d10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('atributo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.Column('descripcion', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_atributo_descripcion'), 'atributo', ['descripcion'], unique=False)
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(length=64), nullable=True),
    sa.Column('platform_token_type', sa.String(length=30), nullable=True),
    sa.Column('platform_access_token', sa.String(length=64), nullable=True),
    sa.Column('store_id', sa.String(length=64), nullable=True),
    sa.Column('company_main_language', sa.String(length=20), nullable=True),
    sa.Column('company_main_currency', sa.String(length=20), nullable=True),
    sa.Column('company_country', sa.String(length=20), nullable=True),
    sa.Column('company_name', sa.String(length=64), nullable=True),
    sa.Column('company_url', sa.String(length=120), nullable=True),
    sa.Column('admin_email', sa.String(length=120), nullable=True),
    sa.Column('communication_email', sa.String(length=120), nullable=True),
    sa.Column('communication_email_name', sa.String(length=120), nullable=True),
    sa.Column('logo', sa.String(length=200), nullable=True),
    sa.Column('fondo', sa.String(length=200), nullable=True),
    sa.Column('param_config', sa.String(length=120), nullable=True),
    sa.Column('contact_name', sa.String(length=64), nullable=True),
    sa.Column('contact_phone', sa.String(length=20), nullable=True),
    sa.Column('contact_email', sa.String(length=120), nullable=True),
    sa.Column('correo_usado', sa.String(length=64), nullable=True),
    sa.Column('correo_apikey', sa.String(length=50), nullable=True),
    sa.Column('correo_id', sa.String(length=50), nullable=True),
    sa.Column('correo_test', sa.Boolean(), nullable=True),
    sa.Column('correo_apikey_test', sa.String(length=50), nullable=True),
    sa.Column('correo_id_test', sa.String(length=50), nullable=True),
    sa.Column('shipping_address', sa.String(length=64), nullable=True),
    sa.Column('shipping_number', sa.String(length=64), nullable=True),
    sa.Column('shipping_floor', sa.String(length=64), nullable=True),
    sa.Column('shipping_zipcode', sa.String(length=64), nullable=True),
    sa.Column('shipping_city', sa.String(length=64), nullable=True),
    sa.Column('shipping_province', sa.String(length=64), nullable=True),
    sa.Column('shipping_country', sa.String(length=64), nullable=True),
    sa.Column('shipping_info', sa.String(length=120), nullable=True),
    sa.Column('company_uid', sa.String(length=150), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_store_id'), 'company', ['store_id'], unique=False)
    op.create_index(op.f('ix_company_timestamp'), 'company', ['timestamp'], unique=False)
    op.create_table('customer',
    sa.Column('customer_uid', sa.String(length=150), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('identification', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('number', sa.String(length=35), nullable=True),
    sa.Column('floor', sa.String(length=100), nullable=True),
    sa.Column('zipcode', sa.String(length=8), nullable=True),
    sa.Column('locality', sa.String(length=250), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('province', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('instructions', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('customer_uid')
    )
    op.create_index(op.f('ix_customer_email'), 'customer', ['email'], unique=False)
    op.create_index(op.f('ix_customer_identification'), 'customer', ['identification'], unique=False)
    op.create_index(op.f('ix_customer_name'), 'customer', ['name'], unique=False)
    op.create_index(op.f('ix_customer_timestamp'), 'customer', ['timestamp'], unique=False)
    op.create_table('order',
    sa.Column('order_uid', sa.String(length=150), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.Integer(), nullable=True),
    sa.Column('order_original_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('order_fecha_compra', sa.DateTime(), nullable=True),
    sa.Column('metodo_de_pago', sa.String(length=35), nullable=True),
    sa.Column('tarjeta_de_pago', sa.String(length=25), nullable=True),
    sa.Column('gastos_cupon', sa.Float(), nullable=True),
    sa.Column('gastos_gateway', sa.Float(), nullable=True),
    sa.Column('gastos_shipping_owner', sa.Float(), nullable=True),
    sa.Column('gastos_shipping_customer', sa.Float(), nullable=True),
    sa.Column('gastos_promocion', sa.Float(), nullable=True),
    sa.Column('owner_note', sa.String(length=500), nullable=True),
    sa.Column('salientes', sa.String(length=10), nullable=True),
    sa.Column('customer_id', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_uid')
    )
    op.create_index(op.f('ix_order_timestamp'), 'order', ['timestamp'], unique=False)
    op.create_table('producto',
    sa.Column('order_id', sa.String(length=150), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prod_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('variant', sa.Integer(), nullable=True),
    sa.Column('alto', sa.Float(), nullable=True),
    sa.Column('largo', sa.Float(), nullable=True),
    sa.Column('profundidad', sa.Float(), nullable=True),
    sa.Column('peso', sa.Float(), nullable=True),
    sa.Column('accion', sa.String(length=10), nullable=True),
    sa.Column('accion_reaccion', sa.Boolean(), nullable=True),
    sa.Column('accion_cambiar_por', sa.Integer(), nullable=True),
    sa.Column('accion_cambiar_por_prod_id', sa.Integer(), nullable=True),
    sa.Column('accion_cambiar_por_desc', sa.String(length=100), nullable=True),
    sa.Column('accion_cantidad', sa.Integer(), nullable=True),
    sa.Column('motivo', sa.String(length=150), nullable=True),
    sa.Column('politica_valida', sa.String(length=50), nullable=True),
    sa.Column('politica_valida_motivo', sa.String(length=100), nullable=True),
    sa.Column('image', sa.String(length=300), nullable=True),
    sa.Column('promo_descuento', sa.Float(), nullable=True),
    sa.Column('promo_nombre', sa.String(length=10), nullable=True),
    sa.Column('promo_precio_final', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id', 'id')
    )
    op.create_index(op.f('ix_producto_prod_id'), 'producto', ['prod_id'], unique=False)
    op.create_index(op.f('ix_producto_timestamp'), 'producto', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_producto_timestamp'), table_name='producto')
    op.drop_index(op.f('ix_producto_prod_id'), table_name='producto')
    op.drop_table('producto')
    op.drop_index(op.f('ix_order_timestamp'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_customer_timestamp'), table_name='customer')
    op.drop_index(op.f('ix_customer_name'), table_name='customer')
    op.drop_index(op.f('ix_customer_identification'), table_name='customer')
    op.drop_index(op.f('ix_customer_email'), table_name='customer')
    op.drop_table('customer')
    op.drop_index(op.f('ix_company_timestamp'), table_name='company')
    op.drop_index(op.f('ix_company_store_id'), table_name='company')
    op.drop_table('company')
    op.drop_index(op.f('ix_atributo_descripcion'), table_name='atributo')
    op.drop_table('atributo')
    # ### end Alembic commands ###
