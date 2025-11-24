import logging
from datetime import datetime

LOG = logging.getLogger()


def build_arxiv_query_url(start_time: datetime, end_time: datetime):

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
