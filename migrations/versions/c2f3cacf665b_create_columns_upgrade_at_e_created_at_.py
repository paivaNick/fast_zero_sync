"""create columns upgrade_at e created_at on todos table

Revision ID: c2f3cacf665b
Revises: 34d6ea02f661
Create Date: 2024-11-22 15:58:54.580042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2f3cacf665b'
down_revision: Union[str, None] = '34d6ea02f661'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column(
        'created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('todos', sa.Column(
        'updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'updated_at')
    op.drop_column('todos', 'created_at')
    # ### end Alembic commands ###