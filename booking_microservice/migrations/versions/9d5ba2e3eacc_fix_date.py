"""fix date

Revision ID: 9d5ba2e3eacc
Revises: b7e66d9d30da
Create Date: 2020-12-13 20:12:54.223758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d5ba2e3eacc'
down_revision = 'b7e66d9d30da'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """UPDATE booking SET booking_date = date('now') WHERE booking_date = 'now()'"""
    )


def downgrade():
    pass
