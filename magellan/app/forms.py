from flask_appbuilder.forms import DynamicForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    BooleanField,
    SelectField,
)
from wtforms.validators import DataRequired


class SearchForm(DynamicForm):
    q = StringField(
        (""),
        validators=[DataRequired()],
        render_kw={"placeholder": "What are you searching for?"},
    )


class CommentForm(DynamicForm):
    comment = TextAreaField(
        ("Add a comment"),
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter a comment...", "rows": 3},
    )
    submit = SubmitField()


class QueryForm(DynamicForm):

    dataset = SelectField("Dataset", coerce=int)
    query = TextAreaField(
        ("SQL Query:"),
        validators=[DataRequired()],
        default=None,
        render_kw={"placeholder": "select * from ...", "rows": 4},
    )
    format = BooleanField("Format query")
    submit = SubmitField("Run Query")

    def __init__(self, query, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)
        self.query.data = query
