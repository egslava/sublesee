from pandas import *

from sublesee.io import (DO_YOU_KNOW,
                         TEXT_WITHOUT_TAGS,
                         AI_SKIP)


def ai_skip(row: str) -> bool:
    return False


def ai_skip_df(df: DataFrame) -> DataFrame:
    df[AI_SKIP] = df[TEXT_WITHOUT_TAGS].apply(ai_skip)
    return df


def read_df(file):
    """df[DO_YOU_KNOW, TEXT_WITHOUT_TAGS]"""
    df = read_excel(file)
    df.columns = df.columns.str.lower()
    df = df[[
        DO_YOU_KNOW,
        TEXT_WITHOUT_TAGS
    ]]
    return df


def read_dfs(files: list[str]) -> DataFrame:
    return concat(read_df(file) for file in files)
