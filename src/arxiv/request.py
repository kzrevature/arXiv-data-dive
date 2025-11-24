import logging
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

LOG = logging.getLogger()


def build_arxiv_query_url(start_time: datetime, end_time: datetime) -> str:
    """
    Builds a valid query url targeting the arXiv API.

    API manual: https://info.arxiv.org/help/api/user-manual.html
    """

    arxiv_api_base_url = "http://export.arxiv.org/api/query"

    if end_time < start_time:
        error_msg = "invalid time range (end_time < start_time)"
        LOG.warning(error_msg)
        raise ValueError(error_msg)

    time_fmt = "%Y%m%d%H%M"
    return (
        f"{arxiv_api_base_url}?"
        "search_query=lastUpdatedDate:"
        f"[{start_time.strftime(time_fmt)}+TO+{end_time.strftime(time_fmt)}]"
        "&max_results=1000"
        "&sortBy=submittedDate&sortOrder=ascending"
    )


def fetch_articles_from_arxiv_api(start_time: datetime, end_time: datetime) -> ET:
    """
    Fetches a list of article entries from the arXiv API date
    which were last updated within the given time range.

    Returns the resulting XML.
    """
    query_url = build_arxiv_query_url(start_time, end_time)
    response = requests.get(query_url)

    return ET.fromstring(response.text)
