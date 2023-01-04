import dataclasses
import sys

import pysrt
from pandas import DataFrame
from dataclasses import dataclass

from pysrt import SubRipItem

AI_SKIP = 'Easy?\n(auto)'.lower()
DO_YOU_KNOW = 'You\nknow?'.lower()
IDX = 'idx'
START = 'start'
END = 'end'
TEXT_WITHOUT_TAGS = 'original'
OUTPUT = 'output'


def _sub_to_row(sub: SubRipItem, break_lines):
    maxsplit = -1 if break_lines else 0
    texts, texts_without_tags = [
        sub.text.split('\n', maxsplit),
        sub.text_without_tags.split('\n', maxsplit),
    ]

    time = str(sub).split('\n')[1]
    # start, stop = time.split(' --> ')
    # str(sub.start)
    return [
        (False, False,  # do you already know it?
         sub.index, sub.start, sub.end,
         text_without_tags, text,)
        for text, text_without_tags in
        zip(
            texts,
            texts_without_tags,
        )
    ]


def read_srt(path, break_lines: bool):
    import pysrt, pandas as pd, numpy as np

    subs = pysrt.open(path)

    subs = [
        row
        for sub in subs
        for row in _sub_to_row(sub, break_lines)
    ]

    df = pd.DataFrame(
        subs,
        columns=[
            AI_SKIP,
            DO_YOU_KNOW,
            IDX,
            START,
            END,
            TEXT_WITHOUT_TAGS,
            OUTPUT,
        ]
    )
    df = df.astype({
        AI_SKIP: np.bool_,
        DO_YOU_KNOW: np.bool_,
        IDX: int,
        START: str,
        END: str,
        TEXT_WITHOUT_TAGS: str,
        OUTPUT: str,
    })
    return df


def write_xslx(filename: str, df: DataFrame):
    import pandas as pd

    writer = pd.ExcelWriter(filename,
                            engine='xlsxwriter', )
    df.to_excel(writer,
                index=False,
                freeze_panes=(1, 1),
                # engine='xlsxwriter',
                sheet_name='Sheet 1',
                )
    sheet = writer.sheets['Sheet 1']
    h, w = df.shape
    sheet.autofilter(0, 0, h, w - 1)

    sheet.set_column(0, 0, 0)
    sheet.set_column(2, 2, options={'hidden': True})
    sheet.set_column(4, 4, options={'hidden': True})
    sheet.set_row(2, 100)
    writer.close()


def read_xlsx(filename: str):
    from pandas import read_excel
    df = read_excel(filename,
                    usecols=[IDX, START, END,
                             OUTPUT])
    return (
        df.groupby(by=[IDX, START, END]).agg(
            {OUTPUT: '\n'.join}
        ).reset_index(level=[IDX, START, END])
    )


def write_srt(filename: str, df: DataFrame):
    file = pysrt.SubRipFile()
    for row in df.itertuples():
        file.append(
            pysrt.SubRipItem(
                row.idx,
                row.start,
                row.end,
                row.output
            )
        )

    file.save(filename)


if __name__ == '__main__' or 'pytest' in sys.modules:
    import doctest

    doctest.testmod()
