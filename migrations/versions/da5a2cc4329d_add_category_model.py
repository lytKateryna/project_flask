"""add category model

Revision ID: da5a2cc4329d
Revises: 731ab92ebf9e
Create Date: 2026-05-10 00:34:48.122722
"""

from alembic import op
import sqlalchemy as sa


revision = "da5a2cc4329d"
down_revision = "731ab92ebf9e"
branch_labels = None
depends_on = None


def upgrade():
    # Если таблица category уже есть, оставляем только изменение длины name
    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=150),
            type_=sa.String(length=50),
            existing_nullable=False
        )


def downgrade():
    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=50),
            type_=sa.String(length=150),
            existing_nullable=False
        )