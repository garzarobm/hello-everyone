"""add annual mileage limit to vehicles

Revision ID: f1a2b3c4d5e6
Revises: ee92897cc33b
Create Date: 2026-04-27 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a2b3c4d5e6'
down_revision = 'ee92897cc33b'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    vehicle_cols = [c['name'] for c in inspector.get_columns('vehicles')]

    cols_to_add = []
    if 'annual_mileage_limit' not in vehicle_cols:
        cols_to_add.append(sa.Column('annual_mileage_limit', sa.Float(), nullable=True))
    if 'annual_mileage_start_date' not in vehicle_cols:
        cols_to_add.append(sa.Column('annual_mileage_start_date', sa.Date(), nullable=True))

    if cols_to_add:
        with op.batch_alter_table('vehicles', schema=None) as batch_op:
            for col in cols_to_add:
                batch_op.add_column(col)


def downgrade():
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_column('annual_mileage_start_date')
        batch_op.drop_column('annual_mileage_limit')
