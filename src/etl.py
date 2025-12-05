from datetime import datetime

from db.connection import Pg8000Connection
from db.queries import select_most_recent_updated_at
from services.extractors import fetch_articles
from services.sync_article import sync_article

# the first arXiv articles were last updated in 1986
DEFAULT_BACKFILL_START_DATE = datetime(1986, 1, 1)


def etl_backfill(backfill_start: datetime, backfill_end: datetime):
    """
    Runs a backfill ETL process which ingests all arXiv articles between two dates and
    loads them into the Article table.

    Makes many HTTP requests so it may take some time to complete.
    """

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


def etl_backfill_auto():
    """
    Runs the ETL backfill process. Automatically selects start and end dates by the
    following rules:
      - Start date is the most recent (by updated_at) article in the Article table, or
        Jan 1, 1986 if the table is empty.
      - End date is datetime.now().
    """

    conn = Pg8000Connection()
    backfill_start = select_most_recent_updated_at(conn)
    conn.close()
    if backfill_start is None:
        backfill_start = DEFAULT_BACKFILL_START_DATE

    backfill_end = datetime.now()

    etl_backfill(backfill_start, backfill_end)
