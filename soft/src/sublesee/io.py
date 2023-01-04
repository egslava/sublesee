import dataclasses
import sys

import pysrt
from pandas import DataFrame
from dataclasses import dataclass

from pysrt import SubRipItem

DO_YOU_KNOW = 'You know?'
IDX = 'idx'
TIME = 'time'
TEXT_WITHOUT_TAGS = 'original'
TEXT = 'output'


def _sub_to_row(sub: SubRipItem, break_lines=False):
    if break_lines:
        texts, texts_without_tags = [
            sub.text.split('\n'),
            sub.text_without_tags.split('\n'),
        ]
    else:
        texts, texts_without_tags = [
            [sub.text],
            [sub.text_without_tags],
        ]

    time = str(sub).split('\n')[1]
    return [
        (False,  # do you already know it?
         sub.index, time, text_without_tags, text,)
        for text, text_without_tags in
        zip(
            texts,
            texts_without_tags,
        )
    ]


def read_srt(path, break_lines: bool = False):
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
            DO_YOU_KNOW,
            IDX,
            TIME,
            TEXT_WITHOUT_TAGS,
            TEXT,
        ]
    )
    df = df.astype({
        DO_YOU_KNOW: np.bool_,
        IDX: int,
        TIME: str,
        TEXT_WITHOUT_TAGS: str,
        TEXT: str,
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
    sheet.set_column(1, 1, options={'hidden': True})
    sheet.set_column(2, 2, options={'hidden': True})
    sheet.set_row(2, 100)
    writer.close()


def read_xlsx(filename: str):
    from pandas import read_excel
    df = read_excel(filename,
                    usecols=['idx', 'time', 'output'])
    return (
        df.groupby(by=['idx', 'time']).agg(
            {'output': '\n'.join}
        ).reset_index(level=['idx', 'time'])
    )


def write_srt(filename: str, df: DataFrame):
    file = pysrt.SubRipFile()
    for row in df.itertuples():
        file.append(
            pysrt.SubRipItem(
                row.idx,
                *row.time.split(' --> '),
                row.output
            )
        )

    file.save(filename)


if __name__ == '__main__' or 'pytest' in sys.modules:
    import doctest

    doctest.testmod()
