"""create posts table

Revision ID: 9f8c1ed4afa4
Revises: 981fd9f65ac3
Create Date: 2022-03-03 13:50:18.970086

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9f8c1ed4afa4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', sa.Column('id',
                           sa.Integer(),
                           nullable=False,
                           primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
