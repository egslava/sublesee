import sys
import time

import pysrt
from pandas import DataFrame

DO_YOU_KNOW = 'You know?'
IDX = 'idx'
TIME = 'time'
TEXT_WITHOUT_TAGS = 'original'
TEXT = 'output'


def read_srt(path):
    import pysrt, pandas as pd, numpy as np
    subs = pysrt.open(path)

    subs = list(
        (
            False,  # do you already know it?
            sub.index,
            str(sub).split('\n')[1],  # time
            sub.text_without_tags.split('\n')[i_spl],
            sub.text.split('\n')[i_spl],
        )
        for sub in subs
        for i_spl, _ in enumerate(sub.text.split('\n'))
    )

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
    # Changing the timezone to +1
    __import__('os').environ['TZ'] = "+01:00"
    time.tzset()
    import doctest

    doctest.testmod()
