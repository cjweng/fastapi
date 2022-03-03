"""add last few coloums to posts table

Revision ID: 6d4d72ace387
Revises: b2d6d54fdc7f
Create Date: 2022-03-03 15:59:55.110146

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6d4d72ace387'
down_revision = 'b2d6d54fdc7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published',
                  sa.Boolean(),
                  nullable=False,
                  server_default='TRUE'),
    )
    op.add_column(
        'posts',
        sa.Column('created_at',
                  sa.TIMESTAMP(timezone=True),
                  nullable=False,
                  server_default=sa.text('NOW()')),
    )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass