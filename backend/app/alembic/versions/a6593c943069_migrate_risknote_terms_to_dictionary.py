"""migrate_risknote_terms_to_dictionary

Revision ID: a6593c943069
Revises: d9b04e9ef8d5
Create Date: 2026-02-27 14:03:27.897959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6593c943069'
down_revision = 'd9b04e9ef8d5'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Group terms into a nested 'terms' object
    # We cast to jsonb to use the grouping and existence operators
    op.execute("""
        UPDATE risknote
        SET cover_snapshot = (cover_snapshot::jsonb || jsonb_build_object('terms', 
            jsonb_strip_nulls(jsonb_build_object(
                'benefits_and_limits', cover_snapshot::jsonb->'benefits_and_limits',
                'excesses', cover_snapshot::jsonb->'excesses',
                'special_clauses', cover_snapshot::jsonb->'special_clauses'
            ))
        ))::json
        WHERE cover_snapshot::jsonb ? 'benefits_and_limits' 
           OR cover_snapshot::jsonb ? 'excesses' 
           OR cover_snapshot::jsonb ? 'special_clauses';
    """)
    
    # 2. Remove legacy top-level keys
    op.execute("""
        UPDATE risknote
        SET cover_snapshot = (cover_snapshot::jsonb - 'benefits_and_limits' - 'excesses' - 'special_clauses')::json
        WHERE cover_snapshot::jsonb ? 'benefits_and_limits' 
           OR cover_snapshot::jsonb ? 'excesses' 
           OR cover_snapshot::jsonb ? 'special_clauses';
    """)


def downgrade():
    # 1. Pull terms back to top level
    op.execute("""
        UPDATE risknote
        SET cover_snapshot = ((cover_snapshot::jsonb || (cover_snapshot::jsonb->'terms')) - 'terms')::json
        WHERE cover_snapshot::jsonb ? 'terms';
    """)
