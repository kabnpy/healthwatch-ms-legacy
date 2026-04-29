"""convert enums to varchar

Revision ID: 223936b03d2f
Revises: e765bc387434
Create Date: 2026-04-28 08:40:27.773148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '223936b03d2f'
down_revision = 'e765bc387434'
branch_labels = None
depends_on = None


def upgrade():
    # Convert Enum columns to VARCHAR to avoid case-sensitivity and missing value issues
    op.alter_column('claim', 'status', type_=sa.String(), postgresql_using="status::text")
    op.alter_column('claimevent', 'event_type', type_=sa.String(), postgresql_using="event_type::text")
    op.alter_column('document', 'entity_type', type_=sa.String(), postgresql_using="entity_type::text")
    op.alter_column('document', 'document_type', type_=sa.String(), postgresql_using="document_type::text")
    op.alter_column('invoice', 'status', type_=sa.String(), postgresql_using="status::text")
    op.alter_column('policy', 'status', type_=sa.String(), postgresql_using="status::text")
    op.alter_column('product', 'pricing_strategy', type_=sa.String(), postgresql_using="pricing_strategy::text")
    op.alter_column('receipt', 'status', type_=sa.String(), postgresql_using="status::text")
    op.alter_column('risknote', 'status', type_=sa.String(), postgresql_using="status::text")
    op.alter_column('risknote', 'transaction_type', type_=sa.String(), postgresql_using="transaction_type::text")


def downgrade():
    # Downgrade is not easily possible as we would need to know the exact Enum values at this point
    pass
