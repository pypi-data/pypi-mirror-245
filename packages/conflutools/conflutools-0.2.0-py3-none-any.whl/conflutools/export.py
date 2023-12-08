from loguru import logger as log
from markdownify import markdownify as md


def page_tree(cfc, page_id):
    """Export page with the given ID and all children recursively.

    The page body will be exported *raw* (as retrieved from Confluence) into a
    file having an `html` suffix and the page ID as the name. Additionally, the
    body will be converted into markdown and stored in a file with an `md`
    suffix.

    IDs and title of all exported pages will be added to `space_index.yaml` for
    easier reference.

    Parameters
    ----------
    cfc : atlassian.Confluence
        The confluence connection object.
    page_id : int or int-like
        The page ID of the root page of the tree to be exported.
    """
    page_id = int(page_id)
    id_index = {}
    page = cfc.get_page_by_id(page_id, expand="body.storage")
    filename_html = f"{page_id}.html"
    filename_md = f"{page_id}.md"
    html = page["body"]["storage"]["value"]
    markdown = md(html)
    with open(filename_html, "w", encoding="utf-8") as outfile:
        outfile.write(html)
    with open(filename_md, "w", encoding="utf-8") as outfile:
        outfile.write(markdown)
    title = page["title"]

    id_index[page_id] = title

    log.success(f"Saved [{filename_html}] and [{filename_md}]: '{title}'")

    children = cfc.get_child_pages(page_id)
    for child in children:
        child_index = page_tree(cfc, child["id"])
        id_index = id_index | child_index

    return id_index
