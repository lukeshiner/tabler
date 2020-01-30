from pathlib import Path

import pytest
import requests_mock

from tabler import CSV, CSVURL, Table

from ...test_tools import TablerTestTools, TableTypeTestTools


class TestCSV:
    BASIC_FILE_PATH = Path(__file__).parent / "testfile.csv"
    WITH_NULLS_PATH = Path(__file__).parent / "testfile_empties.csv"
    WITH_INCOMPLETE_ROW = Path(__file__).parent / "testfile_incomplete_rows.csv"
    WITH_LONG_ROW = Path(__file__).parent / "testfile_long_rows.csv"
    TEST_FORMATTING = Path(__file__).parent / "test_format.csv"
    expected_formatting = ["0", "0", "None", "893275023572039"]

    def test_open(self):
        table = Table(self.BASIC_FILE_PATH, table_type=CSV())
        TablerTestTools.table_valid(table)

    def test_write(self, tmpdir):
        TableTypeTestTools.write_with_table_type(CSV(), tmpdir)

    def test_read_null_values(self):
        TableTypeTestTools.read_null_values_with_tabletype(CSV(), self.WITH_NULLS_PATH)

    def test_formatting(self):
        TableTypeTestTools.format_with_table_type(
            CSV(), self.TEST_FORMATTING, self.expected_formatting
        )

    def test_write_null_values(self, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red", "", "Blue"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test.csv")))
        expected = "Col1,Col2,Col3\nRed,,Blue\nOrange,Yellow,Magenta\n"
        table.write(filepath=str(path))
        with open(str(path), "r") as f:
            assert f.read() == expected

    def test_read_incomplete_rows(self):
        TableTypeTestTools.read_incomplete_rows_with_table_type(
            CSV(), self.WITH_INCOMPLETE_ROW
        )

    def test_write_incomplete_rows(self, tmpdir):
        TableTypeTestTools.write_incomplete_rows_with_table_type(CSV(), tmpdir)

    def test_read_long_rows(self):
        TableTypeTestTools.read_long_rows_with_table_type(CSV(), self.WITH_LONG_ROW)

    def test_open_file_without_table_type(self):
        TablerTestTools.table_valid(Table(str(Path(__file__).parent / "testfile.csv")))

    def test_write_long_rows_with(self, tmpdir):
        TableTypeTestTools.write_long_rows_with_table_type(CSV(), tmpdir)

    def test_save_file_without_extension(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile"
        path = str(tmpdir.join(filename))
        table.write(filepath=path, table_type=CSV())
        assert Path(path + ".csv").exists()

    def test_save_file_without_table_type(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile.csv"
        path = Path(str(tmpdir)) / filename
        table.write(filepath=str(path))
        assert path.exists()

    def test_open_tab_delimited_csv(self):
        path = Path(__file__).parent / "testfile_tab.csv"
        TablerTestTools.table_valid(Table(path, CSV(delimiter="\t")))

    def test_open_csv_with_txt_extension(self):
        path = Path(__file__).parent / "testfile.txt"
        TablerTestTools.table_valid(Table(path, CSV()))

    def test_write_csv_with_no_header(self, tmpdir):
        table = TablerTestTools.basic_table()
        path = Path(str(tmpdir.join("table_with_no_header.csv")))
        table.header = {}
        table.write(filepath=path, table_type=CSV())
        with open(path) as f:
            file_text = f.read()
        expected = "Red,Green,Blue\nOrange,Yellow,Magenta\n"
        assert file_text == expected


class TestCSVURL:
    tabletype = CSVURL()

    def test_open(self):
        with requests_mock.Mocker() as m:
            with open(str(Path(__file__).parent / "testfile.csv"), "rb") as f:
                m.get("http://test.com/testfile.csv", content=f.read())
            table = Table("http://test.com/testfile.csv", table_type=CSVURL())
        TablerTestTools.table_valid(table)

    def test_empty_content(self):
        with requests_mock.Mocker() as m:
            m.get("http://test.com/testfile.csv", content=b"")
            with pytest.raises(ValueError):
                Table("http://test.com/testfile.csv", table_type=CSVURL())

    def test_write(self, tmpdir):
        table = TablerTestTools.basic_table()
        with pytest.raises(NotImplementedError):
            table.write("path", table_type=self.tabletype)
