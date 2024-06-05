"""removed unique name

Revision ID: 3a3224673545
Revises: 9ad9b27c4df8
Create Date: 2024-06-05 19:19:47.435181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a3224673545'
down_revision = '9ad9b27c4df8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('type', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('size', sa.String(length=30), nullable=False))
        batch_op.add_column(sa.Column('abs_path', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('rel_path', sa.String(length=256), nullable=False))
        batch_op.drop_index('ix_document_f_size')
        batch_op.drop_index('ix_document_f_type')
        batch_op.drop_constraint('uix_f_name_f_type', type_='unique')
        batch_op.create_index(batch_op.f('ix_document_size'), ['size'], unique=False)
        batch_op.create_index(batch_op.f('ix_document_type'), ['type'], unique=False)
        batch_op.create_unique_constraint('uix_name_type', ['name', 'type'])
        batch_op.drop_column('f_type')
        batch_op.drop_column('f_content')
        batch_op.drop_column('f_name')
        batch_op.drop_column('f_rel_path')
        batch_op.drop_column('f_abs_path')
        batch_op.drop_column('f_size')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('f_size', sa.VARCHAR(length=30), nullable=False))
        batch_op.add_column(sa.Column('f_abs_path', sa.VARCHAR(length=256), nullable=False))
        batch_op.add_column(sa.Column('f_rel_path', sa.VARCHAR(length=256), nullable=False))
        batch_op.add_column(sa.Column('f_name', sa.VARCHAR(length=128), nullable=False))
        batch_op.add_column(sa.Column('f_content', sa.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('f_type', sa.VARCHAR(length=128), nullable=False))
        batch_op.drop_constraint('uix_name_type', type_='unique')
        batch_op.drop_index(batch_op.f('ix_document_type'))
        batch_op.drop_index(batch_op.f('ix_document_size'))
        batch_op.create_unique_constraint('uix_f_name_f_type', ['f_name', 'f_type'])
        batch_op.create_index('ix_document_f_type', ['f_type'], unique=False)
        batch_op.create_index('ix_document_f_size', ['f_size'], unique=False)
        batch_op.drop_column('rel_path')
        batch_op.drop_column('abs_path')
        batch_op.drop_column('size')
        batch_op.drop_column('type')
        batch_op.drop_column('content')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
