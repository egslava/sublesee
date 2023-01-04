import pandas
import pysrt
import pytest

from unittest import TestCase
from glob import glob

import os
from tempfile import gettempdir, TemporaryFile, \
    NamedTemporaryFile

from sublesee.io import read_srt, write_xslx, \
    read_xlsx, write_srt

FILENAMES = glob('tests/subs/*')


def test_read_srt():
    df = read_srt('tests/subs/1.Eng.srt')
    with TemporaryFile() as file:
        write_xslx(file, df)


def test_write_srt():
    df = read_xlsx('tests/trans/1.Eng.srt.xlsx')
    with NamedTemporaryFile() as file:
        write_srt(file.name, df)


def test_integration():
    with NamedTemporaryFile() as xlsx, \
            NamedTemporaryFile() as srt:
        write_xslx(xlsx.name,
                   read_srt('tests/subs/1.Eng.srt'))

        write_srt(srt.name, read_xlsx(xlsx.name))
        srt_before = pysrt.open('tests/subs/1.Eng.srt')
        srt_after = pysrt.open(srt.name)
        assert srt_before == srt_after


@pytest.mark.parametrize('filename', FILENAMES)
def test_csv_from_zip(filename):
    # assert does not fail
    with open(filename, 'rb') as file:
        bytes = file.read()
        # csv_from_zip(bytes)
