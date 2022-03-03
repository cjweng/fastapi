"""add content column to post table

Revision ID: cb3867628c46
Revises: 9f8c1ed4afa4
Create Date: 2022-03-03 15:32:18.766352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb3867628c46'
down_revision = '9f8c1ed4afa4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
