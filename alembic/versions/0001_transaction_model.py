"""transaction model

Revision ID: 0001
Revises: 
Create Date: 2025-01-11 18:49:38.438845

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE transaction_currency_enum AS ENUM('USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'INR')")
    op.create_table('transaction',
    sa.Column('transaction_id', sa.String(length=300), nullable=False),
    sa.Column('user_id', sa.String(length=300), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', postgresql.ENUM('USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'INR', name='transaction_currency_enum', create_type=False), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('removed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('guid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('transaction_id')
    )


def downgrade():
    op.drop_table('transaction')
    op.execute('DROP TYPE IF EXISTS transaction_currency_enum;')