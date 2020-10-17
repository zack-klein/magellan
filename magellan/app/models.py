import enum

from sqlalchemy.orm import relationship

from magellan.app.database import db, SearchableMixin


class DataItemTypes(enum.Enum):
    view = "VIEW"
    table = "TABLE"
    csv = "CSV"
    file = "FILE"


class DataSourceTypes(enum.Enum):
    s3_bucket = "S3 Bucket"
    sqlalchemy = "SQLAlchemy Connection"


class DataSource(db.Model, SearchableMixin):
    """
    A connection to a database via SQLAlchemy.
    """

    __searchable__ = ["name", "description", "type"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(180))
    connection_string = db.Column(db.String(300))
    type = db.Column(db.Enum(DataSourceTypes), nullable=False)
    extras = db.Column(db.Text)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def to_searchable(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
        }


data_source_rules_dataset_tags = db.Table(
    "data_source_rules_dataset_tags",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "data_source_rule_id",
        db.Integer(),
        db.ForeignKey("data_source_rule.id"),
    ),
    db.Column("tag_id", db.Integer(), db.ForeignKey("dataset_tag.id")),
)


class DataSourceRule(db.Model, SearchableMixin):
    """
    A rule that all datasets under a data source must follow.
    """

    __searchable__ = ["name", "description", "tags"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(500))
    data_source_id = db.Column(
        db.Integer, db.ForeignKey("data_source.id"), nullable=False
    )
    data_source = relationship("DataSource")
    tags = relationship(
        "DatasetTag",
        secondary=data_source_rules_dataset_tags,
        backref="data_source_rule",
        doc="Rules that datasets in this data source must follow.",
    )

    def to_searchable(self):
        return {
            "name": self.name,
            "description": self.description,
            "tags": " ".join([t.name for t in self.tags]),
        }


# Many to many table between datasets and tags
datasets_dataset_tags = db.Table(
    "datasets_dataset_tags",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("dataset_id", db.Integer(), db.ForeignKey("dataset.id")),
    db.Column("tag_id", db.Integer(), db.ForeignKey("dataset_tag.id")),
)


class Dataset(db.Model, SearchableMixin):
    """
    A human created semantic layer created on top of a data item.
    """

    __searchable__ = ["name", "description", "type", "tags"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    schema = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum(DataItemTypes), nullable=False)
    data_source_id = db.Column(
        db.Integer, db.ForeignKey("data_source.id"), nullable=False
    )
    data_source = relationship("DataSource")
    tags = relationship(
        "DatasetTag",
        secondary=datasets_dataset_tags,
        backref="dataset",
        doc="Attributes of this data set.",
    )

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def to_searchable(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "tags": " ".join([t.name for t in self.tags]),
            "data_source": self.data_source.name,
        }


class DatasetTag(db.Model, SearchableMixin):
    """
    Attributes that can be added to a dataset.
    """

    __searchable__ = ["name"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def to_searchable(self):
        return {
            "name": self.name,
        }


class DatasetComment(db.Model, SearchableMixin):
    """
    Comments on datasets.
    """

    __searchable__ = ["comments"]

    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(300), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("ab_user.id"), nullable=False
    )
    user = relationship("User")
    dataset_id = db.Column(
        db.Integer, db.ForeignKey("dataset.id"), nullable=False
    )
    dataset = relationship("Dataset")
    commented_at = db.Column(db.DateTime, nullable=False)

    def __str__(self):
        return f"{self.user.username} (Comment)"

    def __repr__(self):
        return f"{self.user.username} (Comment)"

    def to_searchable(self):
        return {
            "comment": self.comment,
        }
