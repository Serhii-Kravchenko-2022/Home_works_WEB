"""'Init'

Revision ID: ef76ed1aa06e
Revises: 360ef6f12cb5
Create Date: 2023-01-16 12:25:49.767033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef76ed1aa06e'
down_revision = '360ef6f12cb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('grades_student_id_fkey', 'grades', type_='foreignkey')
    op.create_foreign_key(None, 'grades', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.create_foreign_key('grades_student_id_fkey', 'grades', 'groups', ['student_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###