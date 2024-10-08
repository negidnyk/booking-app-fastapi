"""empty message

Revision ID: 9a4f66ae1dbb
Revises: 
Create Date: 2024-09-13 01:12:20.027567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4f66ae1dbb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_oauth_user_account_id', table_name='oauth_user')
    op.drop_index('ix_oauth_user_id', table_name='oauth_user')
    op.drop_index('ix_oauth_user_oauth_name', table_name='oauth_user')
    op.drop_table('oauth_user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oauth_user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('oauth_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('access_token', sa.VARCHAR(length=1024), autoincrement=False, nullable=False),
    sa.Column('expires_at', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('refresh_token', sa.VARCHAR(length=1024), autoincrement=False, nullable=True),
    sa.Column('account_id', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('account_email', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='oauth_user_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='oauth_user_pkey')
    )
    op.create_index('ix_oauth_user_oauth_name', 'oauth_user', ['oauth_name'], unique=False)
    op.create_index('ix_oauth_user_id', 'oauth_user', ['id'], unique=True)
    op.create_index('ix_oauth_user_account_id', 'oauth_user', ['account_id'], unique=False)
    # ### end Alembic commands ###
