import pandas
import pysrt
import pytest

from unittest import TestCase
from glob import glob

from os import path
from tempfile import gettempdir, TemporaryFile, \
    NamedTemporaryFile, TemporaryDirectory

from sublesee.io import read_srt, write_xslx, \
    read_xlsx, write_srt

FILENAMES = glob('tests/subs/*')


@pytest.fixture()
def tempdir():
    with TemporaryDirectory() as dir:
        yield dir
    pass


def test_read_srt():
    df = read_srt('tests/subs/1.Eng.srt')
    with TemporaryFile() as outfile:
        write_xslx(outfile, df)


def test_write_srt(tempdir: str):
    df = read_xlsx('tests/trans/1.Eng.srt.xlsx')
    write_srt(path.join(tempdir, 'out.srt'), df)


def test_integration(tempdir: str):
    srt_name = path.join(tempdir, 'out.srt')

    with NamedTemporaryFile() as xlsx:
        write_xslx(xlsx,
                   read_srt('tests/subs/1.Eng.srt'))

        write_srt(srt_name, read_xlsx(xlsx))
        srt_before = pysrt.open('tests/subs/1.Eng.srt')
        srt_after = pysrt.open(srt_name)
        assert srt_before == srt_after


@pytest.mark.parametrize('filename', FILENAMES)
def test_csv_from_zip(filename):
    # assert does not fail
    with open(filename, 'rb') as file:
        bytes = file.read()
        # csv_from_zip(bytes)
