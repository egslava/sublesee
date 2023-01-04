import pytest, glob
from pandas import DataFrame

from sublesee.ai_skip import (
    read_df, read_dfs, ai_skip_df
)
from sublesee.io import TEXT_WITHOUT_TAGS, DO_YOU_KNOW, \
    AI_SKIP
from sklearn.metrics import (
    precision_score as precision,
    recall_score as recall,
    classification_report,
    confusion_matrix,
)


@pytest.fixture()
def df():
    return read_dfs(glob.glob('tests/ai_skip/*'))


def test_ai_skip_df(df: DataFrame):
    ai_skip_df(df)


def test_metrics(df: DataFrame):
    df = ai_skip_df(df)
    df['ai_think_you_know'] = -1*df[AI_SKIP]+1
    Ys = df[DO_YOU_KNOW], df['ai_think_you_know']

    print('Precision: ', precision(*Ys))
    print('Recall: ', recall(*Ys))
    print(classification_report(*Ys))
    print(confusion_matrix(*Ys))
    assert recall(*Ys) >= 0.95
    assert precision(*Ys) >= 0
