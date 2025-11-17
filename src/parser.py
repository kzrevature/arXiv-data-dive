from .article import Article

from xml.etree import ElementTree as ET


def parse_entry_to_article(node: ET.Element):
    for child in node:
        if child.tag.endswith("id"):
            url = child.text
            id_ = parse_id_from_url(url)
        elif child.tag.endswith("title"):
            title = child.text
        elif child.tag.endswith("published"):
            created_at = child.text
        elif child.tag.endswith("updated"):
            updated_at = child.text

    return Article(id_, title, created_at, updated_at)


def parse_id_from_url(article_url):
    return article_url.split("/")[-1].split("v")[0]
