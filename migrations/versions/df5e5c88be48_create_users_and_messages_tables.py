"""create users and messages tables

Revision ID: df5e5c88be48
Revises: de516238c8d1
Create Date: 2026-06-28 16:12:31.939185

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'df5e5c88be48'
down_revision: Union[str, Sequence[str], None] = 'de516238c8d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True,
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('encrypted_message', sa.String(), nullable=False),
        sa.Column('hached_passwd', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('messages', if_exists=True)
    op.drop_table('users', if_exists=True)
