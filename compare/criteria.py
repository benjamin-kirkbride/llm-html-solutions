import itertools
from typing import NamedTuple


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
