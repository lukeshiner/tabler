from pathlib import Path

from tabler import XLSX, Table

from ...test_tools import TablerTestTools, TableTypeTestTools


class TestXLSX:
    tabletype = XLSX()

    BASIC_FILE_PATH = Path(__file__).parent / "testfile.xlsx"
    WITH_NULLS_PATH = Path(__file__).parent / "testfile_empties.xlsx"
    WITH_INCOMPLETE_ROW = Path(__file__).parent / "testfile_incomplete_rows.xlsx"
    WITH_LONG_ROW = Path(__file__).parent / "testfile_long_rows.xlsx"
    TEST_FORMATTING = Path(__file__).parent / "test_format.xlsx"
    expected_formatting = [0, 0, "None", 893275023572039]

    def test_open(self):
        table = Table(self.BASIC_FILE_PATH, table_type=XLSX())
        TablerTestTools.table_valid(table)

    def test_write(self, tmpdir):
        TableTypeTestTools.write_with_table_type(XLSX(), tmpdir)

    def test_read_null_values(self):
        TableTypeTestTools.read_null_values_with_tabletype(XLSX(), self.WITH_NULLS_PATH)

    def test_formatting(self):
        TableTypeTestTools.format_with_table_type(
            XLSX(), self.TEST_FORMATTING, self.expected_formatting
        )

    def test_write_null_values(self, tmpdir):
        TableTypeTestTools.write_null_values_with_table_type(XLSX(), tmpdir)

    def test_read_incomplete_rows(self):
        TableTypeTestTools.read_incomplete_rows_with_table_type(
            XLSX(), self.WITH_INCOMPLETE_ROW
        )

    def test_write_incomplete_rows(self, tmpdir):
        TableTypeTestTools.write_incomplete_rows_with_table_type(XLSX(), tmpdir)

    def test_read_long_rows(self):
        TableTypeTestTools.read_long_rows_with_table_type(XLSX(), self.WITH_LONG_ROW)

    def test_open_file_without_table_type(self):
        TablerTestTools.table_valid(Table(str(Path(__file__).parent / "testfile.xlsx")))

    def test_write_long_rows_with(self, tmpdir):
        TableTypeTestTools.write_long_rows_with_table_type(XLSX(), tmpdir)

    def test_save_file_without_extension(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile"
        path = str(tmpdir.join(filename))
        table.write(filepath=path, table_type=XLSX())
        assert Path(path + ".xlsx").exists()

    def test_save_file_without_table_type(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile.csv"
        path = Path(str(tmpdir)) / filename
        table.write(filepath=str(path))
        assert path.exists()
