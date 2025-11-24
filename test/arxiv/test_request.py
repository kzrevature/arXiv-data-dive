import logging
from datetime import datetime

import pytest

from arxiv.request import build_arxiv_query_url


def test_build_arxiv_query_url_builds_correct_url():
    start_time = datetime(2025, 1, 1)
    end_time = datetime(2025, 2, 1, 22, 33)

    expected = (
        "http://export.arxiv.org/api/query?search_query=lastUpdatedDate:"
        "[202501010000+TO+202502012233]&max_results=1000&sortBy=submittedDate&sortOrder=ascending"
    )

    actual = build_arxiv_query_url(start_time, end_time)

    assert expected == actual


def test_build_arxiv_query_url_rejects_invalid_time_range(caplog):
    start_time = datetime(2020, 1, 1)
    end_time = datetime(2019, 1, 1)

    with pytest.raises(ValueError):
        build_arxiv_query_url(start_time, end_time)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.WARNING
