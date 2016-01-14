"""empty message

Revision ID: efda2eb78202
Revises: 35f512126236
Create Date: 2016-01-13 23:00:55.448456

"""

# revision identifiers, used by Alembic.
revision = 'efda2eb78202'
down_revision = '35f512126236'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile_serving_url')
    op.drop_column('user', 'profile_url')
    op.drop_column('user', 'recommendation')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('recommendation', mysql.VARCHAR(collation=u'utf8_bin', length=100), nullable=True))
    op.add_column('user', sa.Column('profile_url', mysql.VARCHAR(collation=u'utf8_bin', length=2000), nullable=True))
    op.add_column('user', sa.Column('profile_serving_url', mysql.VARCHAR(collation=u'utf8_bin', length=2200), nullable=True))
    ### end Alembic commands ###