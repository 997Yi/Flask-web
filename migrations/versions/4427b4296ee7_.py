"""empty message

Revision ID: 4427b4296ee7
Revises: 
Create Date: 2020-05-17 23:39:59.833845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4427b4296ee7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    # ### end Alembic commands ###
