import itertools
from typing import NamedTuple

COLUMNS = [
    "html-all-characters",
    "html-all-words",
    "html-all-tokens",
    "html-body-characters",
    "html-body-words",
    "html-body-tokens",
    "html-content-characters",
    "html-content-words",
    "html-content-tokens",
    "strip_tags-all-characters",
    "strip_tags-all-words",
    "strip_tags-all-tokens",
    "strip_tags-body-characters",
    "strip_tags-body-words",
    "strip_tags-body-tokens",
    "strip_tags-content-characters",
    "strip_tags-content-words",
    "strip_tags-content-tokens",
    "markdown-all-characters",
    "markdown-all-words",
    "markdown-all-tokens",
    "markdown-body-characters",
    "markdown-body-words",
    "markdown-body-tokens",
    "markdown-content-characters",
    "markdown-content-words",
    "markdown-content-tokens",
]


class Column(NamedTuple):
    column: str
    format: str
    section: str
    measurement: str


def gen_columns() -> list[Column]:
    formats = ["html", "strip_tags", "markdown"]
    sections = ["all", "body", "content"]
    criteria = ["characters", "words", "tokens"]
    format_criteria_pairs = itertools.product(formats, sections, criteria)
    columns: list[Column] = []
    for format, section, criterion in format_criteria_pairs:
        if format == "strip_tags" and section == "all":
            # `strip_tags` does not support `all` section
            continue

        column_title = f"{format}-{section}-{criterion}"
        column = Column(
            column=column_title,
            format=column_title.split("-")[0],
            section=column_title.split("-")[1],
            measurement=column_title.split("-")[2],
        )
        columns.append(column)

    return tuple(columns)
