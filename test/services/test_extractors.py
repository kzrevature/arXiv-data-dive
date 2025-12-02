# functionality that should be tested

from datetime import datetime
from unittest.mock import patch

import pytest

from article import Article
from arxiv.parser import ArticleParseResult
from services.extractors import fetch_articles

DUMMY_DATE = datetime(2000, 2, 2)
DUMMY_URL = "https://arxiv.org/abs/phys/1234"
DUMMY_ARTICLE = Article("phys/1234", "Title", DUMMY_DATE, DUMMY_DATE)
DUMMY_ARTICLE_2 = Article("math/5678", "Title", DUMMY_DATE, DUMMY_DATE)


@pytest.fixture(autouse=True)
def sleep_mock():
    with patch("services.extractors.time.sleep") as mock:
        yield mock


@pytest.fixture()
def fetch_mock():
    with patch("services.extractors.fetch_articles_from_arxiv_api") as mock:
        yield mock


@pytest.fixture()
def extract_total_mock():
    with patch("services.extractors.extract_total_results") as mock:
        yield mock


@pytest.fixture()
def extract_entries_mock():
    with patch("services.extractors.extract_article_entries") as mock:
        yield mock


@pytest.fixture()
def parse_entry_mock():
    with patch("services.extractors.parse_entry_to_article") as mock:
        yield mock


def test_fetch_articles_stops_when_entries_match_total(
    sleep_mock,
    fetch_mock,
    extract_total_mock,
    extract_entries_mock,
    parse_entry_mock,
):
    extract_total_mock.side_effect = [28, 18, 8, 0, 0]
    extract_entries_mock.side_effect = [
        [DUMMY_ARTICLE] * 10,
        [DUMMY_ARTICLE] * 10,
        [DUMMY_ARTICLE] * 8,
        [],
        [],
    ]

    # how many pages until finding one where total = len(entries)
    expected_fetch_count = 3
    # only sleep between calls
    expected_sleep_count = expected_fetch_count - 1

    for _ in fetch_articles(DUMMY_DATE, DUMMY_DATE):
        pass

    assert fetch_mock.call_count == expected_fetch_count
    assert extract_total_mock.call_count == expected_fetch_count
    assert extract_entries_mock.call_count == expected_fetch_count
    assert sleep_mock.call_count == expected_sleep_count


def test_fetch_articles_only_yields_successful_parses(
    fetch_mock,
    extract_total_mock,
    extract_entries_mock,
    parse_entry_mock,
):
    extract_total_mock.return_value = 3
    extract_entries_mock.return_value = [None, None, None]

    parse_entry_mock.side_effect = [
        ArticleParseResult(True, DUMMY_ARTICLE, DUMMY_URL),
        ArticleParseResult(False, None, DUMMY_URL),
        ArticleParseResult(True, DUMMY_ARTICLE_2, DUMMY_URL),
    ]

    expected = [DUMMY_ARTICLE, DUMMY_ARTICLE_2]

    actual = list(fetch_articles(DUMMY_DATE, DUMMY_DATE))

    assert parse_entry_mock.call_count == 3
    assert actual == expected


def test_fetch_articles_parses_all_fetched(
    fetch_mock,
    extract_total_mock,
    extract_entries_mock,
    parse_entry_mock,
):
    page_lens = [2, 7, 4, 3]

    extract_total_mock.side_effect = [sum(page_lens[i:]) for i in range(len(page_lens))]
    extract_entries_mock.side_effect = [[DUMMY_ARTICLE] * l_ for l_ in page_lens]
    parse_entry_mock.return_value = ArticleParseResult(True, DUMMY_ARTICLE, "url")

    expected_parse_count = sum(page_lens)

    for _ in fetch_articles(DUMMY_DATE, DUMMY_DATE):
        pass

    assert parse_entry_mock.call_count == expected_parse_count
