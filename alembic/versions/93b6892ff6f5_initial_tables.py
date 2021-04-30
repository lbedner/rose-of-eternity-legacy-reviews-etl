"""initial tables

Revision ID: 93b6892ff6f5
Revises: 
Create Date: 2021-04-29 22:33:51.199783

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '93b6892ff6f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'review',
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('user_name', sa.String(50), nullable=False),
        sa.Column('score', sa.Float, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('date', postgresql.TIMESTAMP(precision=6), nullable=False),
        sa.Column('date_added', postgresql.TIMESTAMP(precision=6), server_default=sa.func.now(), nullable=False),
        sa.Column('date_modified', postgresql.TIMESTAMP(precision=6), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('review')
