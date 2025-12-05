import logging
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from arxiv.request import build_arxiv_query_url, fetch_articles_from_arxiv_api

DUMMY_DATE = datetime(2022, 2, 2)


@pytest.fixture
def build_query_mock():
    with patch("arxiv.request.build_arxiv_query_url") as mock:
        yield mock


@pytest.fixture
def http_get_mock():
    with patch("arxiv.request.requests.get") as mock:
        yield mock


@pytest.fixture
def etree_fromstring_mock():
    with patch("arxiv.request.ET.fromstring") as mock:
        yield mock


def test_build_arxiv_query_url_builds_correct_url():
    start_time = datetime(2025, 1, 1)
    end_time = datetime(2025, 2, 1, 22, 33)

    expected = (
        "http://export.arxiv.org/api/query?search_query=lastUpdatedDate:"
        "[202501010000+TO+202502012233]&max_results=777&sortBy=lastUpdatedDate&sortOrder=ascending"
    )

    actual = build_arxiv_query_url(start_time, end_time, 777)

    assert expected == actual


def test_build_arxiv_query_url_rejects_invalid_time_range(caplog):
    start_time = datetime(2020, 1, 1)
    end_time = datetime(2019, 1, 1)

    with pytest.raises(ValueError):
        build_arxiv_query_url(start_time, end_time, 10)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.WARNING


def test_fetch_articles_from_arxiv_api_builds_query_with_correct_args(
    build_query_mock, http_get_mock, etree_fromstring_mock
):
    input_date_1 = datetime(2000, 1, 2)
    input_date_2 = datetime(2000, 3, 4)
    max_results = 234
    fetch_articles_from_arxiv_api(input_date_1, input_date_2, max_results)
    build_query_mock.assert_called_once_with(input_date_1, input_date_2, max_results)


def test_fetch_articles_from_arxiv_api_makes_request_with_correct_url(
    build_query_mock, http_get_mock, etree_fromstring_mock
):
    sample_url = "sample-query-url.com"
    build_query_mock.return_value = sample_url

    fetch_articles_from_arxiv_api(DUMMY_DATE, DUMMY_DATE, 0)

    http_get_mock.assert_called_once_with(sample_url)


def test_fetch_articles_from_arxiv_api_parses_http_response_to_xml_string(
    http_get_mock, etree_fromstring_mock
):
    sample_xml = "<xml>sample xml</xml>"
    sample_response = Mock()
    sample_response.text = sample_xml
    http_get_mock.return_value = sample_response
    fetch_articles_from_arxiv_api(DUMMY_DATE, DUMMY_DATE, 0)

    etree_fromstring_mock.assert_called_once_with(sample_xml)


def test_fetch_articles_from_arxiv_api_respects_max_results_threshold(
    http_get_mock, etree_fromstring_mock
):
    # doesn't error
    fetch_articles_from_arxiv_api(DUMMY_DATE, DUMMY_DATE, 1000)
    # errors
    with pytest.raises(ValueError):
        fetch_articles_from_arxiv_api(DUMMY_DATE, DUMMY_DATE, 1001)
