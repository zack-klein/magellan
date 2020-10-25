"""Initial migration.

Revision ID: f17210d52107
Revises:
Create Date: 2020-10-25 09:11:05.087049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f17210d52107"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "data_source",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=180), nullable=True),
        sa.Column("connection_string", sa.String(length=300), nullable=True),
        sa.Column(
            "type",
            sa.Enum("s3_bucket", "sqlalchemy", name="datasourcetypes"),
            nullable=False,
        ),
        sa.Column("extras", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "dataset_tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "data_source_rule",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("data_source_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_source.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("schema", sa.String(length=300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "type",
            sa.Enum("view", "table", "csv", "file", name="dataitemtypes"),
            nullable=False,
        ),
        sa.Column("data_source_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_source.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "data_source_rules_dataset_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data_source_rule_id", sa.Integer(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["data_source_rule_id"],
            ["data_source_rule.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["dataset_tag.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dataset_comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("comment", sa.String(length=300), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("commented_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ab_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "datasets_dataset_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["dataset_tag.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("datasets_dataset_tags")
    op.drop_table("dataset_comment")
    op.drop_table("data_source_rules_dataset_tags")
    op.drop_table("dataset")
    op.drop_table("data_source_rule")
    op.drop_table("dataset_tag")
    op.drop_table("data_source")
    # ### end Alembic commands ###
