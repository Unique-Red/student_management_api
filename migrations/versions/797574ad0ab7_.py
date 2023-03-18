"""empty message

Revision ID: 797574ad0ab7
Revises: 1303251bb8a7
Create Date: 2023-03-17 15:18:51.593700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '797574ad0ab7'
down_revision = '1303251bb8a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_courses')
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_code', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('course_title', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('course_unit', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('lecturer', sa.String(length=120), nullable=False))
        batch_op.drop_column('name')
        batch_op.drop_column('description')

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('matric_number', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('gpa', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('grade')
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('grade', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.drop_column('gpa')
        batch_op.drop_column('matric_number')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=120), nullable=False))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), nullable=False))
        batch_op.drop_column('lecturer')
        batch_op.drop_column('course_unit')
        batch_op.drop_column('course_title')
        batch_op.drop_column('course_code')

    op.create_table('_alembic_tmp_courses',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('course_code', sa.VARCHAR(length=80), nullable=False),
    sa.Column('course_title', sa.VARCHAR(length=120), nullable=False),
    sa.Column('course_unit', sa.INTEGER(), nullable=False),
    sa.Column('lecturer', sa.VARCHAR(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###