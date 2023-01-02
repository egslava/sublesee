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
        xlsx=DEFAULT_XLSX_PATH
):
    """
    :param srt: a path to input srt file
    :param xlsx: a path to output xlsx
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