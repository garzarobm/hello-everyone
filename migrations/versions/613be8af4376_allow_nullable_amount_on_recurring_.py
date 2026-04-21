"""Allow nullable amount on recurring_expenses

Revision ID: 613be8af4376
Revises: 998cdb1497c6
Create Date: 2026-02-27 11:00:38.154072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '613be8af4376'
down_revision = '998cdb1497c6'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'recurring_expenses' not in inspector.get_table_names():
        return
    amount_col = next(
        (c for c in inspector.get_columns('recurring_expenses') if c['name'] == 'amount'),
        None,
    )
    if amount_col is not None and amount_col.get('nullable') is True:
        return

    with op.batch_alter_table('recurring_expenses', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.FLOAT(),
               nullable=True)


def downgrade():
    with op.batch_alter_table('recurring_expenses', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.FLOAT(),
               nullable=False)
