"""add listing and profile fields

Revision ID: a4d8e92b6f31
Revises: ed39766d59b2
Create Date: 2026-09-11
"""

from alembic import op
import sqlalchemy as sa


revision = "a4d8e92b6f31"
down_revision = "ed39766d59b2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("whatsapp_number", sa.String(length=20), nullable=True))
    op.add_column("properties", sa.Column("listing_type", sa.String(length=10), nullable=False, server_default="sale"))
    op.add_column("properties", sa.Column("neighborhood", sa.String(length=100), nullable=True))
    op.add_column("properties", sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    with op.batch_alter_table("properties") as batch_op:
        batch_op.drop_column("is_featured")
        batch_op.drop_column("neighborhood")
        batch_op.drop_column("listing_type")
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("whatsapp_number")
