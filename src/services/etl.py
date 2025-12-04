from datetime import datetime

from db.connection import Pg8000Connection
from services.extractors import fetch_articles
from services.sync_article import sync_article


def etl_backfill(backfill_start: datetime, backfill_end=None):
    """
    Runs a backfill ETL process which ingests all arXiv articles between two dates and
    loads them into the Article table. If the end boundary is not supplied, use datetime.now().

    Makes many HTTP requests so it may take some time to complete.
    """

    if backfill_end is None:
        backfill_end = datetime.now()

    conn = Pg8000Connection()

    # extraction loop
    for article in fetch_articles(backfill_start, backfill_end):
        # load into db
        try:
            sync_article(conn, article)
        # handle failed validation
        except ValueError:
            # TODO log and handle these errors
            pass

    conn.close()
