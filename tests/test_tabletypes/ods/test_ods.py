from pathlib import Path

from tabler import ODS

from ..test_tabletype import TableTypeTest


class TestODS(TableTypeTest):
    tabletype = ODS()

    BASIC_FILE_PATH = Path(__file__).parent / "testfile.ods"
    WITH_NULLS_PATH = Path(__file__).parent / "testfile_empties.ods"
    WITH_INCOMPLETE_ROW = Path(__file__).parent / "testfile_incomplete_rows.ods"
    WITH_LONG_ROW = Path(__file__).parent / "testfile_long_rows.ods"
    TEST_FORMATTING = Path(__file__).parent / "test_format.ods"
