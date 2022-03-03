"""add user table

Revision ID: 9c93c5832836
Revises: cb3867628c46
Create Date: 2022-03-03 15:41:20.448808

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c93c5832836'
down_revision = 'cb3867628c46'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at',
                  sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'),
                  nullable=False), 
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
