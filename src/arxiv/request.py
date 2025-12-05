import logging
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

LOG = logging.getLogger()

# hardcoded cap on the max_results param in API queries
# the API can technically support up to 30000 but smaller values run faster and are easier to test
API_RESULTS_CAP = 1000


def build_arxiv_query_url(
    start_time: datetime,
    end_time: datetime,
    max_results: int,
) -> str:
    """
    Builds a valid query url targeting the arXiv API.

    API manual: https://info.arxiv.org/help/api/user-manual.html
    """

    if max_results > API_RESULTS_CAP:
        raise ValueError(
            f"max_results value of {max_results} exceeds the maximum {API_RESULTS_CAP}"
        )

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
        f"&max_results={max_results}"
        "&sortBy=lastUpdatedDate&sortOrder=ascending"
    )


def fetch_articles_from_arxiv_api(
    start_time: datetime,
    end_time: datetime,
    max_results: int = API_RESULTS_CAP,
) -> ET.Element:
    """
    Fetches a list of article entries from the arXiv API date
    which were last updated within the given time range.

    Returns the resulting XML.
    """
    query_url = build_arxiv_query_url(start_time, end_time, max_results)
    response = requests.get(query_url)

    return ET.fromstring(response.text)
