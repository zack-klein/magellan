import enum

from flask_login import current_user

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


roles_data_source = db.Table(
    "roles_data_source",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "data_source",
        db.Integer(),
        db.ForeignKey("data_source.id"),
    ),
    db.Column("role_id", db.Integer(), db.ForeignKey("ab_role.id")),
)

data_source_tags = db.Table(
    "data_source_tags",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "data_source",
        db.Integer(),
        db.ForeignKey("data_source.id"),
    ),
    db.Column("tag_id", db.Integer(), db.ForeignKey("dataset_tag.id")),
)


class DataSource(db.Model, SearchableMixin):
    """
    A connection to a database via SQLAlchemy.
    """

    __searchable__ = ["name", "description", "type"]
    __type__ = "source"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(180))
    connection_string = db.Column(db.String(300))
    type = db.Column(db.Enum(DataSourceTypes), nullable=False)
    extras = db.Column(db.Text)
    roles = relationship(
        "Role",
        secondary=roles_data_source,
        backref="data_source",
        doc="Roles that are allowed to see this data source.",
    )
    tags = relationship(
        "DatasetTag",
        secondary=data_source_tags,
        backref="data_source_tags",
        doc="Tags for this dataset.",
    )
    icon = "fa-database"

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
        }

    def user_has_access(self):

        for role in self.roles:

            if role in current_user.roles:
                return True

        return False


# Many to many table between datasets and tags
datasets_dataset_tags = db.Table(
    "datasets_dataset_tags",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("dataset_id", db.Integer(), db.ForeignKey("dataset.id")),
    db.Column("tag_id", db.Integer(), db.ForeignKey("dataset_tag.id")),
)


roles_dataset = db.Table(
    "roles_dataset",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "dataset",
        db.Integer(),
        db.ForeignKey("dataset.id"),
    ),
    db.Column("role_id", db.Integer(), db.ForeignKey("ab_role.id")),
)


class Dataset(db.Model, SearchableMixin):
    """
    A human created semantic layer created on top of a data item.
    """

    __searchable__ = ["name", "description", "type", "tags"]
    __type__ = "dataset"

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
    roles = relationship(
        "Role",
        secondary=roles_dataset,
        backref="dataset",
        doc="Roles that are allowed to see this data set.",
    )
    icon = "fa-table"

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

    def user_has_access(self):

        for role in self.data_source.roles:

            if role in current_user.roles:
                return True

        return False


class DatasetTag(db.Model, SearchableMixin):
    """
    Attributes that can be added to a dataset.
    """

    __searchable__ = ["name"]
    __type__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    icon = "fa-tag"

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
    __type__ = "comment"

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
    icon = "fa-comment"

    def __str__(self):
        return f"{self.user.username} (Comment)"

    def __repr__(self):
        return f"{self.user.username} (Comment)"

    def to_searchable(self):
        return {
            "comment": self.comment,
        }
