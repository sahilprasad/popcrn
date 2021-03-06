"""adding sentiment table and tweet-to-sentiment association table

Revision ID: f857527a8ebe
Revises: 9cd5befa5647
Create Date: 2016-05-11 18:43:28.930253

"""

# revision identifiers, used by Alembic.
revision = 'f857527a8ebe'
down_revision = '9cd5befa5647'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sentiment',
    sa.Column('sentiment_id', sa.Integer, nullable=False, autoincrement=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('sentiment_id')
    )
    op.create_table('association',
    sa.Column('tweet_id', sa.String(length=50), nullable=True),
    sa.Column('sentiment_id', sa.Integer, nullable=True),
    sa.ForeignKeyConstraint(['sentiment_id'], ['sentiment.sentiment_id'], ),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.tweet_id'], )
    )
    op.add_column(u'tweet', sa.Column('max_sentiment_word', sa.String(length=150), nullable=True))
    op.add_column(u'tweet', sa.Column('min_sentiment_word', sa.String(length=150), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'tweet', 'min_sentiment_word')
    op.drop_column(u'tweet', 'max_sentiment_word')
    op.drop_table('association')
    op.drop_table('sentiment')
    ### end Alembic commands ###
