"""Tests for tabler.Table class."""

import pytest

from tabler import Table


class TableTest:

    TEST_HEADER = ("Col1", "Col2", "Col3")
    TEST_ROW_1 = ["Red", "Green", "Blue"]
    TEST_ROW_2 = ["Orange", "Yellow", "Magenta"]
    TEST_DATA = [TEST_ROW_1, TEST_ROW_2]

    def is_valid_table(self, table):
        assert len(table.header) == 3
        assert len(table) == 2
        assert all([len(row) == 3 for row in table])
        assert table.header == self.TEST_HEADER
        assert list(table.rows[0]) == self.TEST_ROW_1
        assert list(table.rows[1]) == self.TEST_ROW_2
        assert table[0]["Col1"] == "Red"

    def get_basic_table(self):
        header = self.TEST_HEADER
        data = self.TEST_DATA
        return Table(header=header, data=data)


class TestTable(TableTest):
    def test_create_table_with_header_and_data(self):
        table = self.get_basic_table()
        self.is_valid_table(table)

    def test_create_table_no_args_raises(self):
        with pytest.raises(TypeError):
            Table()

    def test_access_cell_by_header_column_index(self):
        table = self.get_basic_table()
        assert table[0][0] == "Red"

    def test_access_cell_by_header_name_column_index(self):
        table = self.get_basic_table()
        assert table[0]["Col1"] == "Red"

    def test_change_cell_value(self):
        table = self.get_basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = "Green"
        assert table[0]["Col1"] == "Green"

    def test_get_table_column(self):
        table = self.get_basic_table()
        assert table.get_column("Col1") == ["Red", "Orange"]
