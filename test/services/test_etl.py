from datetime import datetime
from unittest.mock import MagicMock, call, patch

from article import Article
from services.etl import etl_backfill

DUMMY_DATE = datetime(2042, 4, 2)
DUMMY_ARTICLE_1 = Article("id/001", "Title 1", DUMMY_DATE, DUMMY_DATE)
DUMMY_ARTICLE_2 = Article("id/002", "Title 2", DUMMY_DATE, DUMMY_DATE)
DUMMY_ARTICLE_3 = Article("id/003", "Title 3", DUMMY_DATE, DUMMY_DATE)


@patch("services.etl.fetch_articles")
@patch("services.etl.sync_article")
@patch("services.etl.Pg8000Connection")
def test_etl_backfill(conn_init_mock, sync_mock, fetch_gen_mock):
    expected_start_date = datetime(2020, 1, 1)
    expected_end_date = datetime(2050, 1, 1)

    fetch_gen_mock.return_value = iter(
        [DUMMY_ARTICLE_1, DUMMY_ARTICLE_2, DUMMY_ARTICLE_3]
    )
    conn_mock = MagicMock()
    conn_init_mock.return_value = conn_mock

    etl_backfill(expected_start_date, expected_end_date)

    fetch_gen_mock.assert_called_once_with(expected_start_date, expected_end_date)
    sync_mock.assert_has_calls(
        [
            call(conn_mock, DUMMY_ARTICLE_1),
            call(conn_mock, DUMMY_ARTICLE_2),
            call(conn_mock, DUMMY_ARTICLE_3),
        ]
    )


@patch("services.etl.datetime")
@patch("services.etl.fetch_articles")
@patch("services.etl.Pg8000Connection")
def test_etl_backfill_defaults_to_present(
    conn_init_mock, fetch_gen_mock, datetime_mock
):
    expected_start_date = datetime(2020, 1, 1)
    expected_end_date = datetime(2050, 1, 1)
    datetime_mock.now.return_value = expected_end_date

    fetch_gen_mock.return_value = iter([])

    etl_backfill(expected_start_date)

    fetch_gen_mock.assert_called_once_with(expected_start_date, expected_end_date)
