"""Markdata - Block converters
"""
import csv
import json
import os

import yaml

from typing import List, Tuple
from .converters import to_html_table

DIRECTIVES = {}


class DIRECTIVE(object):
    """CONVERTER keeps track of all the ``@CONVERTER`` functions.
    """

    def __init__(self, f):
        DIRECTIVES[f.__name__] = f


def _read(path, parse=False):
    """Read the contents of the given file.
    """
    _, ext = os.path.splitext(path)
    with open(os.path.abspath(path)) as f:
        data = _parse(f, ext) if parse else f.read()
    return data


def _parse(data, ext):
    """Convert the contents of a structured file into a `dict` object.
    """
    if ext == ".json":
        return json.load(data)
    elif ext in (".yml", ".yaml"):
        return yaml.load(data)
    elif ext == ".csv":
        return csv.DictReader(data)


@DIRECTIVE
def table(path: str, classes: List[str] = [], caption: str = "") -> str:
    """Return an HTML table built from structured data (CSV, JSON, or YAML).

    `path` [required]: A path (relative to the directive-containing file) to a
           CSV, JSON, or YAML file.

    `classes` [optional]: A list of HTML classes to apply to the table.

    `caption` [optional]: A caption for the table.

    Example:
        `table{'path': 'table.yml', 'classes': ['table'], 'caption': '...'}`
    """
    rows = []
    for i, row in enumerate(_read(path, parse=True)):
        if i == 0:
            rows.append(row.keys())
        rows.append(row.values())
    return to_html_table(rows, caption, classes)


@DIRECTIVE
def document(path: str, span: Tuple[int, int] = []) -> str:
    """Return the contents of a document (or part of it).

    `path` [required]: A path (relative to the directive-containing file) to a
           local file.

    `span` [optional]: A tuple ([begin, end]) indicating the beginning and
           ending line of the snippet (defaults to the entire file).

    Example:
        `document{'path': 'my_file.py', 'span': [10, 13]}`
    """
    text = _read(path)
    if span:
        text = "\n".join(text.splitlines()[span[0] - 1 : span[1]])
    return text
