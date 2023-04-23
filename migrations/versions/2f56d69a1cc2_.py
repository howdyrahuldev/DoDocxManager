"""empty message

Revision ID: 2f56d69a1cc2
Revises: 446a118d4c05
Create Date: 2023-04-02 03:38:31.317966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f56d69a1cc2'
down_revision = '446a118d4c05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_me', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Website', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_me', schema=None) as batch_op:
        batch_op.drop_column('Website')

    # ### end Alembic commands ###
