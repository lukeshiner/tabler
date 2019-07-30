"""Tests for tabler.Table class."""

import os
from pathlib import Path

import pytest

from tabler import CSV, HTML, ODS, XLSX, Table


class TestTable:
    """Tests for tabler.Table class."""

    TEST_CSV_PATH = str(os.path.join(os.path.dirname(__file__), "testfile.csv"))
    TEST_ODS_PATH = str(os.path.join(os.path.dirname(__file__), "testfile.ods"))
    TEST_XLSX_PATH = str(os.path.join(os.path.dirname(__file__), "testfile.xlsx"))

    TEST_HEADER = ["Col1", "Col2", "Col3"]
    TEST_ROW_1 = ["Red", "Green", "Blue"]
    TEST_ROW_2 = ["Orange", "Yellow", "Magenta"]
    TEST_DATA = [TEST_ROW_1, TEST_ROW_2]

    def is_valid_table(self, table):
        """Check tabler.Table object is valid."""
        assert len(table.header) == 3
        assert len(table) == 2
        assert all([len(row) == 3 for row in table])
        assert table.header == self.TEST_HEADER
        assert table.rows[0].row == self.TEST_ROW_1
        assert table.rows[1].row == self.TEST_ROW_2
        assert table[0]["Col1"] == "Red"

    def get_basic_table(self):
        """Create tabler.Table object populated with test data."""
        header = self.TEST_HEADER
        data = self.TEST_DATA
        return Table(header=header, data=data)

    def test_create_table_with_header_and_data(self):
        """Test tabler.Table with test data is valid."""
        table = self.get_basic_table()
        self.is_valid_table(table)

    def test_create_table_no_args_raises(self):
        """Test calling tabler.Table without arguments raises VauleError."""
        with pytest.raises(TypeError):
            Table()

    def test_access_cell_by_header_column_index(self):
        """Test row and column indexes can be used to access cells."""
        table = self.get_basic_table()
        assert table[0][0] == "Red"

    def test_access_cell_by_header_name_column_index(self):
        """Test row index and column name can be used to access cells."""
        table = self.get_basic_table()
        assert table[0]["Col1"] == "Red"

    def test_change_cell_value(self):
        """Test cell data can be updated."""
        table = self.get_basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = "Green"
        assert table[0]["Col1"] == "Green"

    def test_get_table_column(self):
        """Test tabler.Table.get_column method returns column data."""
        table = self.get_basic_table()
        assert table.get_column("Col1") == ["Red", "Orange"]

    def test_open_csv(self):
        """Test tabler.Table can be created from CSV file."""
        table = Table(self.TEST_CSV_PATH, table_type=CSV())
        self.is_valid_table(table)

    def test_open_ods(self):
        """Test tabler.Table can be created from .ods file."""
        table = Table(self.TEST_ODS_PATH, table_type=ODS())
        self.is_valid_table(table)

    def test_open_xlsx(self):
        """Test tabler.Table can be created from .xlsx file."""
        table = Table(self.TEST_XLSX_PATH, table_type=XLSX())
        self.is_valid_table(table)

    def test_save_csv_file(self, tmpdir):
        """Test tabler.Table can create .csv file."""
        table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile.csv"
        table.write(filepath, table_type=CSV())

    def test_save_ods_file(self, tmpdir):
        """Test tabler.Table can create .ods file."""
        table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile.ods"
        table.write(filepath, table_type=ODS())

    def test_save_xlsx_file(self, tmpdir):
        """Test tabler.Table can create .xlsx file."""
        table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile.xlsx"
        table.write(filepath, table_type=XLSX())

    def test_save_html_file(self, tmpdir):
        """Test tabler.Table can create .html file."""
        table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile.html"
        table.write(filepath, table_type=HTML())

    def test_open_file_without_table_type(self):
        """Test valid TableType can be found when writing a file."""
        self.is_valid_table(Table(self.TEST_CSV_PATH))

    def test_save_file_without_extension(self, tmpdir):
        """Test valid extension can be found from TableType."""
        table = self.get_basic_table()
        filename = "testfile"
        path = str(tmpdir.join(filename))
        table.write(filepath=path, table_type=CSV())
        assert Path(path + ".csv").exists()

    def test_save_file_without_table_type(self, tmpdir):
        """Test valid TableType can be found when opening a file."""
        table = self.get_basic_table()
        filename = "testfile.csv"
        path = Path(str(tmpdir)) / filename
        table.write(filepath=str(path))
        assert path.exists()

    def test_open_tab_delimited_csv(self):
        """Test .csv file can be opened with non default delimiter."""
        path = Path(__file__).parent / "testfile_tab.csv"
        self.is_valid_table(Table(path, CSV(delimiter="\t")))

    def test_open_csv_with_txt_extension(self):
        """Test .csv file can be opened with non default file extension."""
        path = Path(__file__).parent / "testfile.txt"
        self.is_valid_table(Table(path, CSV()))
