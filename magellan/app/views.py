import datetime
import random
import sqlparse

from flask import redirect, flash, request, url_for, abort

from flask_login import current_user

from flask_appbuilder import ModelView, expose, BaseView
from flask_appbuilder.actions import action
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count

from magellan.app import models
from magellan.app.database import db
from magellan.app.fab import appbuilder
from magellan.app.forms import SearchForm, CommentForm, QueryForm

from magellan.extractors.main import extract_datasets
from magellan.samplers.main import get_sample_data
from magellan.query import query_dataset, clean_table_name


class SearchView(BaseView):
    route_base = "/search"
    default_view = "search"

    @has_access
    @expose("/", methods=["GET", "POST"])
    def search(self):
        search_form = SearchForm()

        if request.method == "POST":
            # if search_form.validate_on_submit():
            return redirect(
                url_for("SearchView.q", text=request.form.get("q"))
            )

        tags = db.session.query(models.DatasetTag).all()
        random.shuffle(tags)

        return self.render_template(
            "search.html",
            search_form=search_form,
            tags=tags,
        )

    @has_access
    @expose("/q/<string:text>", methods=["GET", "POST"])
    def q(self, text):
        search_form = SearchForm()

        if request.method == "POST":
            return redirect(
                url_for("SearchView.q", text=request.form.get("q"))
            )

        # TODO: Add pagination
        dataset_results, dataset_total = models.Dataset.search(text, 1, 100)
        data_source_results, data_source_total = models.DataSource.search(
            text, 1, 100
        )
        tag_results, tag_total = models.DatasetTag.search(text, 1, 100)
        comment_results, comment_total = models.DatasetComment.search(
            text, 1, 100
        )

        results = []
        results += [d for d in dataset_results if d.user_has_access()]
        results += [d for d in data_source_results if d.user_has_access()]
        results += tag_results
        results += comment_results

        total = len(results)

        return self.render_template(
            "search_results.html",
            results=results,
            total=total,
            search_term=text,
            search_form=search_form,
        )

    @has_access
    @expose("/browse/<int:dataset_id>", methods=["GET", "POST"])
    def browse(self, dataset_id):
        dataset = db.session.query(models.Dataset).get_or_404(dataset_id)

        # Make sure the user has access
        if not dataset.user_has_access():
            abort(403)

        comments = (
            db.session.query(models.DatasetComment)
            .filter(models.DatasetComment.dataset_id == dataset.id)
            .all()
        )
        comment_form = CommentForm()
        sample_data = get_sample_data(dataset)
        if request.method == "POST":
            comment = models.DatasetComment(
                user_id=current_user.id,
                dataset_id=dataset.id,
                comment=request.form.get("comment"),
                commented_at=datetime.datetime.utcnow(),
            )
            db.session.add(comment)
            db.session.commit()
            return redirect(
                url_for("SearchView.browse", dataset_id=dataset.id)
            )

        return self.render_template(
            "browse.html",
            dataset=dataset,
            comment_form=comment_form,
            sample_data=sample_data,
            comments=comments,
        )


class ConsoleView(BaseView):
    route_base = "/console"
    default_view = "console"

    @has_access
    @expose("/", methods=["GET", "POST"])
    def console(self, *args, **kwargs):

        dataset_id = request.args.get("dataset")
        query = request.args.get("q")
        should_format = request.args.get("format")

        if request.method == "POST":
            dataset_id = request.form.get("dataset")
            query = request.form.get("query")
            should_format = request.form.get("format")
            return redirect(
                url_for(
                    "ConsoleView.console",
                    dataset=dataset_id,
                    q=query,
                    format=should_format,
                )
            )

        datasets = db.session.query(models.Dataset).all()
        if dataset_id:
            dataset = (
                db.session.query(models.Dataset)
                .filter(models.Dataset.id == dataset_id)
                .first()
            )
            if not dataset:
                flash(f"Dataset {dataset_id} doesn't exist!", "danger")
        else:
            dataset = None

        if query and should_format:
            query = sqlparse.format(query, reindent=True, keyword_case="upper")

        query_form = QueryForm(query)
        query_form.dataset.choices = [(d.id, d.name) for d in datasets]

        if should_format:
            query_form.format.checked = True

        if dataset:
            query_form.dataset.process_data(dataset.id)
            msg = "Table name: {table}"
            clean_table = clean_table_name(dataset.name)
            query_form.dataset.description = msg.format(table=clean_table)

        if dataset and query:
            results = query_dataset(dataset, query)
        else:
            results = "<p>No results!</p>"

        return self.render_template(
            "console.html",
            query_form=query_form,
            results=results,
        )


class DatasetChartView(GroupByChartView):
    route_base = "/charts"
    datamodel = SQLAInterface(models.Dataset)
    chart_title = "Dataset explorer"

    definitions = [
        {
            "label": "Datasets by Data Source",
            "group": "data_source.name",
            "series": [(aggregate_count, "id")],
        }
    ]


class DataSourceView(ModelView):
    route_base = "/sources"
    datamodel = SQLAInterface(models.DataSource)

    edit_columns = [
        "name",
        "description",
        "type",
        "roles",
    ]

    show_columns = [
        "name",
        "description",
        "type",
    ]

    list_columns = [
        "name",
        "description",
        "type",
    ]

    @action(
        "extract_dataset",
        "Extract datasets",
        "Please confirm dataset extraction.",
        "fa-motorcycle",
    )
    def extract_dataset(self, items):
        """
        Extract datasets from
        """
        for item in items:
            extract_datasets(item)
            msg = (
                f"Data extracted for {item.name}!\n Head to the 'Datasets' "
                "tab to check it out."
            )
            flash(msg, "success")

        return redirect(url_for("DataSourceView.list"))


class DataSourceRuleView(ModelView):
    route_base = "/rules"
    datamodel = SQLAInterface(models.DataSourceRule)

    list_columns = [
        "name",
        "data_source",
        "description",
        "tags",
    ]


class DatasetView(ModelView):
    route_base = "/datasets"
    datamodel = SQLAInterface(models.Dataset)

    list_columns = [
        "name",
        "data_source",
        "description",
        "tags",
    ]

    @action(
        "get_report",
        "Get report",
        "Are you sure you'd like to create a report?",
        "fa-bar-chart",
    )
    def get_report(self, items):
        """
        Get a panda profiler report of any dataset.
        """
        for item in items:
            pass
            # report.to_file(f"{report_title}.html")
        return redirect("/")

    @action(
        "multi_delete",
        "Delete",
        "Are you sure you'd like to delete these records?",
        "fa-trash",
    )
    def multi_delete(self, items):
        """
        Get a panda profiler report of any dataset.
        """
        for item in items:
            db.session.delete(item)

        db.session.commit()
        return redirect("/datasetview/list")


class DatasetTagView(ModelView):
    route_base = "/tags"
    datamodel = SQLAInterface(models.DatasetTag)


appbuilder.add_view(SearchView, "Find Data", icon="fa-search")
appbuilder.add_view(
    DataSourceView,
    "Sources",
    category="Govern",
    category_icon="fa-gavel",
    icon="fa-database",
)
appbuilder.add_view(
    DatasetView, "Datasets", category="Govern", icon="fa-table"
)
appbuilder.add_separator(category="Govern")
appbuilder.add_view(DataSourceRuleView, "Rules", category="Govern")
appbuilder.add_view(DatasetTagView, "Tags", category="Govern", icon="fa-tags")
appbuilder.add_view(
    DatasetChartView,
    "Datasets",
    category="Analyze",
    icon="fa-bar-chart",
    category_icon="fa-lightbulb-o",
)
appbuilder.add_view(
    ConsoleView, "SQL Console", category="Analyze", icon="fa-database"
)
