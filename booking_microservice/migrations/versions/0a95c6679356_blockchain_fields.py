"""blockchain fields

Revision ID: 0a95c6679356
Revises: 9d5ba2e3eacc
Create Date: 2021-02-14 21:07:31.461932

"""
from alembic import op
import sqlalchemy as sa

from booking_microservice.constants import BlockChainStatus

# revision identifiers, used by Alembic.
revision = '0a95c6679356'
down_revision = '9d5ba2e3eacc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    if connection.dialect.name == "postgresql":
        status_enum = postgresql.ENUM(
            'CONFIRMED', 'DENIED', 'PENDING', 'UNSET', 'ERROR', name='blockchain_status'
        )
    else:
        status_enum = sa.Enum(
            'CONFIRMED', 'DENIED', 'PENDING', 'UNSET', 'ERROR', name='blockchain_status'
        )

    status_enum.create(op.get_bind())

    op.add_column('booking', sa.Column('blockchain_id', sa.Integer(), nullable=True))
    op.add_column(
        'booking',
        sa.Column(
            'blockchain_status',
            status_enum,
            nullable=True,
            default=BlockChainStatus.UNSET.value,
            server_default=BlockChainStatus.UNSET.value,
        ),
    )
    op.add_column(
        'booking',
        sa.Column('blockchain_transaction_hash', sa.String(length=512), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('booking', 'blockchain_transaction_hash')
    op.drop_column('booking', 'blockchain_status')
    op.drop_column('booking', 'blockchain_id')
    op.execute("DROP TYPE blockchain_status")
    # ### end Alembic commands ###
