"""Fixed  problems with tables relations

Revision ID: 6cd0ea09a4c9
Revises: d73c996d25cc
Create Date: 2025-01-26 18:56:25.715180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd0ea09a4c9'
down_revision: Union[str, None] = 'd73c996d25cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
