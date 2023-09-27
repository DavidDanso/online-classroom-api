"""create assignments table

Revision ID: de7275515928
Revises: 3ad81acee8e3
Create Date: 2023-09-25 10:15:45.142622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de7275515928'
down_revision: Union[str, None] = '3ad81acee8e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignments',
    sa.Column('assignment_id', sa.Integer(), nullable=False),
    sa.Column('assignment_title', sa.String(), nullable=False),
    sa.Column('assignment_description', sa.String(), nullable=False),
    sa.Column('assignment_questions', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('assignment_instruction', sa.String(), nullable=False),
    sa.Column('due_date', sa.String(), nullable=False),
    sa.Column('max_score', sa.Integer(), nullable=False),
    sa.Column('user_fkey', sa.Integer(), nullable=False),
    sa.Column('course_fkey', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['course_fkey'], ['courses.course_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_fkey'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('assignment_id')
    )
    op.create_index(op.f('ix_assignments_assignment_id'), 'assignments', ['assignment_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assignments_assignment_id'), table_name='assignments')
    op.drop_table('assignments')
    # ### end Alembic commands ###
