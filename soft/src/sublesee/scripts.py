from pathlib import Path
from textwrap import dedent, indent

import clize

from sublesee.io import (
    read_srt, write_xslx,
    read_xlsx, write_srt
)

DEFAULT_HTML_PATH = "{srt}.html"
DEFAULT_XLSX_PATH = "{srt}.xlsx"
DEFAULT_SRT_PATH = "{xlsx}.srt"


def html_boilerplate(body: str):
    return dedent(f"""
        <!doctype html>
        <html>
        <head>
          <meta charset="utf-8">
        </head>
        <body>
        {indent(body, " " * 12)}
        </body>
  """).strip()


def srt2html(
        srt: str,
        html=DEFAULT_HTML_PATH
):
    """
    :param srt: a path to input srt file
    :param html: a path to output html
    """
    import pysrt
    subs = pysrt.open(srt)

    if html == DEFAULT_HTML_PATH:
        html = f"{srt}.html"

    out_path = Path(html)
    out_path.write_text(
        html_boilerplate(
            '\n\n<br/></br>'.join(
                sub.text.replace("\n", "\n</br>")
                for sub in subs
            )
        )
    )


def srt2xlsx(
        srt: str,
        xlsx=DEFAULT_XLSX_PATH,
        break_lines=False,
):
    """
    :param srt: a path to input srt file
    :param xlsx: a path to output xlsx
    :param break_lines: This argument has a story.
    When I started development, I imported srt this
    way: each subtitle = one row in xlsx.

    Then, I decided to change this behavior: one
    subtitle LINE is one xlsx row. It's different
    from previous options, when there're multiline
    subtitles. Thus, each 'screen' can become 1 OR
    more xlsx lines. But because the translator
    couldn't really understand context by such a
    line, I decided to get back to the previous
    version. Then I just decided to let the final
    user  decide how to use it and make the strategy
    as an opt argument.
    """
    if xlsx == DEFAULT_XLSX_PATH:
        xlsx = f"{srt}.xlsx"

    df = read_srt(srt)
    write_xslx(xlsx, df)


def xlsx2srt(
        xlsx: str,
        srt=DEFAULT_SRT_PATH
):
    """
    :param xlsx: a path to input srt file
    :param srt: a path to output xlsx
    """
    if srt == DEFAULT_SRT_PATH:
        srt = f"{xlsx}.srt"

    df = read_xlsx(xlsx)
    write_srt(srt, df)


def run(*args, **kwargs):
    clize.run(srt2html, srt2xlsx, xlsx2srt)
