import pandas
import pysrt
import pytest

from unittest import TestCase
from glob import glob

from pandas import read_excel

from sublesee.io import read_srt, write_xslx, \
    read_xlsx, write_srt

FILENAMES = glob('tests/subs/*')


def test_read_srt():
    df = read_srt('tests/subs/1.Eng.srt')
    write_xslx('tests/subs/1.Eng.xlsx', df)


def test_write_srt():
    df = read_xlsx('tests/trans/1.Eng.srt.xlsx')
    write_srt('tests/trans/1.Eng.srt.xlsx.srt', df)


def test_integrational():
    import os
    try:
        write_xslx('tests/subs/1.Eng.xlsx',
                   read_srt('tests/subs/1.Eng.srt'))

        write_srt('tests/subs/1.Eng.srt.copy',
                  read_xlsx('tests/subs/1.Eng.xlsx'))
        import filecmp
        filecmp.cmp('tests/subs/1.Eng.srt',
                    'tests/subs/1.Eng.srt.copy')
    finally:
        os.remove('tests/subs/1.Eng.srt.copy')


@pytest.mark.parametrize('filename', FILENAMES)
def test_csv_from_zip(filename):
    # assert does not fail
    with open(filename, 'rb') as file:
        bytes = file.read()
        # csv_from_zip(bytes)
