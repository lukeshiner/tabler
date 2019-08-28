from pathlib import Path

from tabler import XLSX

from ..test_tabletype import TableTypeTest


class TestXLSX(TableTypeTest):
    tabletype = XLSX()

    BASIC_FILE_PATH = Path(__file__).parent / "testfile.xlsx"
    WITH_NULLS_PATH = Path(__file__).parent / "testfile_empties.xlsx"
    WITH_INCOMPLETE_ROW = Path(__file__).parent / "testfile_incomplete_rows.xlsx"
    WITH_LONG_ROW = Path(__file__).parent / "testfile_long_rows.xlsx"
