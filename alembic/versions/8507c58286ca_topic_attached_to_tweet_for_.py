"""topic attached to tweet for accessbility to hack

Revision ID: 8507c58286ca
Revises: 681d93c9fb50
Create Date: 2016-05-12 10:41:16.025146

"""

# revision identifiers, used by Alembic.
revision = '8507c58286ca'
down_revision = '681d93c9fb50'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tweet', sa.Column('topic', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_tweet_topic'), 'tweet', ['topic'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tweet_topic'), table_name='tweet')
    op.drop_column('tweet', 'topic')
    ### end Alembic commands ###
