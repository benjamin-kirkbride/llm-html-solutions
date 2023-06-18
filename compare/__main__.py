import csv
import tomllib
from functools import lru_cache

import pypandoc
import requests
import tiktoken
from bs4 import BeautifulSoup
from strip_tags import strip_tags
from yarl import URL

from . import criteria

with open("config.toml", mode="rb") as fp:
    CONFIG = tomllib.load(fp)


def format_html(html: str) -> str:
    return html


@lru_cache
def format_strip_tags(html: str) -> str:
    return strip_tags(input=html, selectors=None)


@lru_cache
def format_markdown(html: str) -> str:
    return pypandoc.convert_text(html, "markdown", format="html")


format = {
    "html": format_html,
    "strip_tags": format_strip_tags,
    "markdown": format_markdown,
}


def get_all(html: str, selector: str) -> str:
    return html


@lru_cache
def get_body(html: str, selector: str) -> str:
    soup = BeautifulSoup(html, "html5lib")
    body_resultset = soup.body.findChildren(recursive=False)
    body = "".join([str(tag) for tag in body_resultset])
    return body


@lru_cache
def get_content(html: str, selectors: str) -> str:
    # TODO: verify this works how I expect
    output_list = []
    soup = BeautifulSoup(html, "html5lib")
    for selector in selectors:
        for tag in soup.select(selector):
            children = tag.findChildren(recursive=False)
            output_list.append("".join([str(tag) for tag in children]))
    output = "".join(output_list)
    return output


section = {
    "all": get_all,
    "body": get_body,
    "content": get_content,
}


def count_characters(text: str) -> int:
    return len(text)


def count_words(text: str) -> int:
    # TODO: this needs fleshed out (or abandoned)
    # more characters
    return len(text.split())


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    count = len(encoding.encode(text))
    return count


measurements = {
    "characters": count_characters,
    "words": count_words,
    "tokens": count_tokens,
}


def main():
    criteria_sets = criteria.gen_columns()
    # TODO: add domain to page name
    columns = ("page_name", "page_url") + tuple(
        criteria_set.column for criteria_set in criteria_sets
    )

    with open("results.csv", "w") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=columns)
        csv_writer.writeheader()

        for webpage in CONFIG["webpages"]:
            print(f"processing {webpage['name']} - {webpage['url']}")
            raw_content_selectors = webpage.get("content_selectors")
            if raw_content_selectors:
                content_selectors = tuple(raw_content_selectors)
            else:
                content_selectors = None

            row = {
                "page_name": webpage["name"],
                "page_url": webpage["url"],
            }

            response = requests.get(webpage["url"])
            html = response.text

            for criteria_set in criteria_sets:
                if any(
                    criteria in criteria_set
                    for criteria in (
                        webpage.get("skipped_columns", [])
                        + webpage.get("skipped_criteria", [])
                    )
                ):
                    print(f"skipping {criteria_set.column}")
                    continue

                if criteria_set.section == "content" and not content_selectors:
                    print(
                        f"'content_selectors' not specified, skipping {criteria_set.column}"
                    )
                    continue

                sectioned_html = section[criteria_set.section](
                    html, content_selectors
                )

                text = format[criteria_set.format](sectioned_html)
                if (
                    "reddit" in webpage["url"]
                    and criteria_set.format == "markdown"
                    and criteria_set.section == "content"
                ):
                    print(text)
                    import sys

                    sys.exit()

                row[criteria_set.column] = measurements[
                    criteria_set.measurement
                ](text)

            csv_writer.writerow(row)


if __name__ == "__main__":
    main()
