"""3

Revision ID: 75556a5baeb5
Revises: 57e6bd9208bc
Create Date: 2024-05-19 21:27:29.586411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75556a5baeb5'
down_revision: Union[str, None] = '57e6bd9208bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
