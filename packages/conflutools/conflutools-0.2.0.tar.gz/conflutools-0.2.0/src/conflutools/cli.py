import yaml
import sys

import click
from loguru import logger as log

from .connection import connect
from . import export


@click.command()
@click.option(
    "--config",
    default="confconf.yaml",
    show_default=True,
    help="Configuration file.",
)
@click.option(
    "--page",
    help=(
        "Page ID or title of the tree root to be exported. When using the page title "
        "it is mandatory to specify '--space' as well."
    ),
    required=True,
)
@click.option(
    "--space",
    help=(
        "Space KEY to request the page from. If this option is given, '--page' "
        "will be interpreted as the title instead of the page ID."
    ),
    default="",
)
def export_tree(config, page, space):
    """Recursively export a page and all of its children to HTML and MD files."""
    cfc = connect(config)

    if not space:
        try:
            page_id = int(page)
        except Exception:
            log.error(f"Invalid page ID: {page}")
            sys.exit(1)
    else:
        try:
            page_id = cfc.get_page_id(space, title=page)
            if not page_id:
                raise RuntimeError
        except Exception:
            log.error(f"Cannot find page [{page}] in space [{space}]!")
            sys.exit(2)

    log.debug(f"Requesting root page ID: {page_id}")

    tree_index = export.page_tree(cfc, page_id=page_id)
    log.success(f"Exported {len(tree_index)} pages.")

    index_fname = "page_index.yaml"
    log.debug(f"Updating page index file: {index_fname}...")
    try:
        with open(index_fname, mode="r", encoding="utf-8") as index_file:
            page_index = yaml.safe_load(index_file)
    except FileNotFoundError:
        page_index = {}

    page_index = page_index | tree_index
    with open(index_fname, mode="w", encoding="utf-8") as index_file:
        yaml.safe_dump(page_index, index_file, width=float("inf"))
    log.success(f"Updated page index file: {index_fname}.")
