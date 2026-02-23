"""Refactor Policy and RiskNote models

Revision ID: c5c580ca4b1f
Revises: 38cad97ed24a
Create Date: 2026-02-23 12:11:28.109039

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'c5c580ca4b1f'
down_revision = '38cad97ed24a'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add risk_details to policy
    op.add_column('policy', sa.Column('risk_details', sa.JSON(), nullable=True))
    
    # 2. Data migration: Copy snapshot from most recent risknote to policy
    # We use a subquery to find the most recent risknote for each policy
    # Note: We check if policy_snapshot exists in risknote table first to be safe
    # although we know it should be there in the down_revision state.
    op.execute("""
        UPDATE policy
        SET risk_details = (
            SELECT policy_snapshot
            FROM risknote
            WHERE risknote.policy_id = policy.id
            ORDER BY risknote.effective_date DESC, risknote.created_at DESC
            LIMIT 1
        )
        WHERE risk_details IS NULL;
    """)
    
    # 3. Alter inception_date to be NOT NULL
    op.alter_column('policy', 'inception_date',
               existing_type=sa.DATE(),
               nullable=False)

    # 4. Remove redundant columns from risknote
    op.drop_column('risknote', 'policy_snapshot')
    op.drop_column('risknote', 'payment_status')


def downgrade():
    # 1. Add columns back to risknote
    op.add_column('risknote', sa.Column('payment_status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('risknote', sa.Column('policy_snapshot', sa.JSON(), autoincrement=False, nullable=True))
    
    # 2. Data migration back: Populate policy_snapshot from policy
    op.execute("""
        UPDATE risknote
        SET policy_snapshot = (
            SELECT risk_details
            FROM policy
            WHERE policy.id = risknote.policy_id
        )
    """)
    
    # 3. Alter inception_date to be nullable
    op.alter_column('policy', 'inception_date',
               existing_type=sa.DATE(),
               nullable=True)
    
    # 4. Drop risk_details from policy
    op.drop_column('policy', 'risk_details')
