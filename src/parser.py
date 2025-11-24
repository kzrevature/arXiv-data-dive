import re
from xml.etree import ElementTree as ET

from article import Article


def parse_entry_to_article(node: ET.Element):
    for child in node:
        if child.tag.endswith("id"):
            url = child.text
            id_ = parse_arxiv_url_to_id(url)
        elif child.tag.endswith("title"):
            title = child.text
        elif child.tag.endswith("published"):
            created_at = child.text
        elif child.tag.endswith("updated"):
            updated_at = child.text

    return Article(id_, title, created_at, updated_at)


def validate_arxiv_id_old_fmt(id_: str) -> bool:
    """
    Check if an string matches the pre-2007 arXiv format for article IDs.

    [cat]/YYMMXXX
    """
    id_sections = id_.split("/")
    if len(id_sections) != 2:
        return False
    # the second part of the id is given in YYMMXXX format
    elif not id_sections[1].isdigit():
        return False
    elif len(id_sections[1]) != 7:
        return False
    return True


def validate_arxiv_id_new_fmt(id_: str) -> bool:
    """
    Check if an string matches the post-2007 arXiv format for article IDs.

    YYMM.XXXX
    YYMM.XXXXX
    """
    id_sections = id_.split(".")
    if len(id_sections) != 2:
        return False
    # the first part of the id is in YYMM format
    elif not id_sections[0].isdigit():
        return False
    elif len(id_sections[0]) != 4:
        return False
    # the second section is a string of 4 or 5 digits
    elif not id_sections[1].isdigit():
        return False
    elif len(id_sections[1]) not in (4, 5):
        return False
    return True


def parse_arxiv_url_to_id(article_url):
    """
    Extracts the unique arXiv identifier for an article based on its abstract url.
    Raises a ValueError if the request is malformed.

    Refer to https://info.arxiv.org/help/arxiv_identifier_for_services.html for more details.
    """

    arxiv_url_prefix = "http://arxiv.org/abs/"

    # check prefix
    if not article_url.startswith(arxiv_url_prefix):
        raise ValueError("arXiv url is malformed: bad prefix")
    article_url = article_url[len(arxiv_url_prefix) :]

    # check version suffix
    suffix_re = "v\\d+$"
    suffix_re_match = re.search(suffix_re, article_url)
    if suffix_re_match:
        article_url = article_url[: suffix_re_match.start()]

    if validate_arxiv_id_new_fmt(article_url) or validate_arxiv_id_old_fmt(article_url):
        return article_url
    else:
        raise ValueError("arXiv url is malformed: bad id")
