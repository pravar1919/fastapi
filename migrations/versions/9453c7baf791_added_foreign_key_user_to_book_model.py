"""added foreign key user to book model

Revision ID: 9453c7baf791
Revises: 647eb1da8865
Create Date: 2024-10-12 10:59:18.368554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9453c7baf791'
down_revision: Union[str, None] = '647eb1da8865'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'book', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'user_id')
    # ### end Alembic commands ###
