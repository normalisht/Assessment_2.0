"""empty message

Revision ID: d75239c34618
Revises: 9dc17551e490
Create Date: 2021-08-26 18:37:46.675455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd75239c34618'
down_revision = '9dc17551e490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('viewer', sa.Column('organization', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('viewer', 'organization')
    # ### end Alembic commands ###
