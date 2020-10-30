"""fix: Remove dataset rules

Revision ID: ae289bc5e317
Revises: f05e2340143e
Create Date: 2020-10-30 01:00:57.880656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ae289bc5e317"
down_revision = "f05e2340143e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "data_source_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data_source", sa.Integer(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["data_source"],
            ["data_source.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["dataset_tag.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("data_source_rules_dataset_tags")
    op.drop_table("data_source_rule")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "data_source_rule",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('data_source_rule_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name", sa.VARCHAR(length=80), autoincrement=False, nullable=True
        ),
        sa.Column(
            "description",
            sa.VARCHAR(length=500),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "data_source_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_source.id"],
            name="data_source_rule_data_source_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="data_source_rule_pkey"),
        sa.UniqueConstraint("name", name="data_source_rule_name_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "data_source_rules_dataset_tags",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "data_source_rule_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("tag_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["data_source_rule_id"],
            ["data_source_rule.id"],
            name="data_source_rules_dataset_tags_data_source_rule_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["dataset_tag.id"],
            name="data_source_rules_dataset_tags_tag_id_fkey",
        ),
        sa.PrimaryKeyConstraint(
            "id", name="data_source_rules_dataset_tags_pkey"
        ),
    )
    op.drop_table("data_source_tags")
    # ### end Alembic commands ###
