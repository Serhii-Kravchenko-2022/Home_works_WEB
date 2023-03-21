"""'Init'

Revision ID: 26066d6f69d7
Revises: 
Create Date: 2023-03-02 13:00:45.531318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26066d6f69d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contacts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'user_id')
    # ### end Alembic commands ###