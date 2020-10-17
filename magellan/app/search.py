import logging

from flask import current_app


logger = logging.getLogger(__name__)


def add_to_index(index, model):
    logger.info(f"Adding {model} to {index}...")
    if not current_app.elasticsearch:
        return
    payload = model.to_searchable()
    # for field in model.__searchable__:
    #
    #     payload[field] = modelattr

    current_app.elasticsearch.index(index=index, id=model.id, body=payload)
    logger.info(f"Added {model} to {index}! ID: {model.id}")


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    logger.info(f"Querying {query} on {index}...")
    search = current_app.elasticsearch.search(
        index=index,
        body={
            "query": {"multi_match": {"query": query, "fields": ["*"]}},
            "from": (page - 1) * per_page,
            "size": per_page,
        },
    )

    logger.info(f"Got len({search}) results!")
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]
