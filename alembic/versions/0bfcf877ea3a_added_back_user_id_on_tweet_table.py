"""added back user_id on tweet table

Revision ID: 0bfcf877ea3a
Revises: 8507c58286ca
Create Date: 2016-05-13 20:01:43.178304

"""

# revision identifiers, used by Alembic.
revision = '0bfcf877ea3a'
down_revision = '8507c58286ca'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tweet', sa.Column('user_id', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_tweet_user_id'), 'tweet', ['user_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tweet_user_id'), table_name='tweet')
    op.drop_column('tweet', 'user_id')
    ### end Alembic commands ###
