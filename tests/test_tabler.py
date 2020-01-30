"""Tests for tabler.Table class."""


from pathlib import Path

import pytest

from tabler import CSV, Table
from tabler.tablerow import TableRow

from .test_tools import TablerTestTools


class TestTable:
    def test_create_table_with_header_and_data(self):
        table = TablerTestTools.basic_table()
        TablerTestTools.table_valid(table)

    def test_create_table_no_args_raises(self):
        with pytest.raises(TypeError):
            Table()

    def test_access_cell_by_header_column_index(self):
        table = TablerTestTools.basic_table()
        assert table[0][0] == "Red"

    def test_access_cell_by_header_name_column_index(self):
        table = TablerTestTools.basic_table()
        assert table[0]["Col1"] == "Red"

    def test_access_cell_with_invalid_key(self):
        table = TablerTestTools.basic_table()
        with pytest.raises(ValueError) as e:
            table[0][5.9]
        assert "Index" in str(e)
        assert "float" in str(e)

    def test_change_cell_value(self):
        table = TablerTestTools.basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = "Green"
        assert table[0]["Col1"] == "Green"

    def test_change_cell_value_by_integer_index(self):
        table = TablerTestTools.basic_table()
        assert table[0][0] == "Red"
        table[0][0] = "Green"
        assert table[0][0] == "Green"

    def test_change_cell_to_float(self):
        table = TablerTestTools.basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = 0.975
        assert table[0]["Col1"] == 0.975

    def test_change_cell_to_int(self):
        table = TablerTestTools.basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = 567
        assert table[0]["Col1"] == 567

    def test_change_cell_to_None(self):
        table = TablerTestTools.basic_table()
        assert table[0]["Col1"] == "Red"
        table[0]["Col1"] = None
        assert table[0]["Col1"] is None

    def test_change_cell_with_invalid_index(self):
        table = TablerTestTools.basic_table()
        with pytest.raises(ValueError) as e:
            table[0][5.9] = 4
        assert "Index" in str(e)
        assert "float" in str(e)

    def test_get_table_column(self):
        table = TablerTestTools.basic_table()
        assert table.get_column("Col1") == ["Red", "Orange"]

    def test_remove_column(self):
        table = TablerTestTools.basic_table()
        table.remove_column("Col2")
        assert table.header == ("Col1", "Col3")
        assert list(table.rows[0]) == ["Red", "Blue"]
        assert list(table.rows[1]) == ["Orange", "Magenta"]

    def test_open_unknown_filetype_without_tabletype_raises(self, tmpdir):
        with pytest.raises(ValueError):
            Table("testfile.unk")

    def test_write_unknown_filetype_without_tabletype_raises(self, tmpdir):
        table = TablerTestTools.basic_table()
        filepath = Path(str(tmpdir)) / "testfile.unk"
        with pytest.raises(ValueError):
            table.write(filepath)

    def test_table__str___and__repr__methods(self):
        table = TablerTestTools.basic_table()
        expected = (
            "Table Object containing 3 colomuns and 2 rows\n"
            "Column Headings: Col1, Col2, Col3"
        )
        assert str(table) == expected
        assert repr(table) == expected

    def test_set_table_type(self, tmpdir):
        header = TablerTestTools.TEST_HEADER
        data = TablerTestTools.TEST_DATA
        table_type = CSV()
        table = Table(header=header, data=data, table_type=table_type)
        assert table.table_type == table_type
        path = Path(str(tmpdir)) / "testfile"
        table.write(path)

    def test_table_is_empty_method(self):
        t = Table(header=[], data=[])
        assert t.is_empty() is True
        t = TablerTestTools.basic_table()
        assert t.is_empty() is False

    def test_table_empty_method(self):
        t = TablerTestTools.basic_table()
        t.empty()
        assert t.is_empty() is True

    def test_table_copy_method(self):
        t1 = TablerTestTools.basic_table()
        t2 = t1.copy()
        assert t1 is not t2
        assert t1[0] is not t2[0]

    def test_table_sort_method_with_string_key(self):
        table = Table(header=("A", "B", "C"), data=((8, 5, 6), (9, 3, 4), (6, 4, 7)))
        table.sort("B")
        assert list(table[0]) == [9, 3, 4]
        assert list(table[1]) == [6, 4, 7]
        assert list(table[2]) == [8, 5, 6]

    def test_table_sort_method_with_integer_key(self):
        table = Table(header=("A", "B", "C"), data=((8, 5, 6), (9, 3, 4), (6, 4, 7)))
        table.sort(1)
        assert list(table[0]) == [9, 3, 4]
        assert list(table[1]) == [6, 4, 7]
        assert list(table[2]) == [8, 5, 6]

    def test_table_sort_method_with_text(self):
        table = Table(
            header=("A", "B", "C"),
            data=(("i", "e", "g"), ("x", "c", "d"), ("f", "d", "g")),
        )
        table.sort("B")
        assert list(table[0]) == ["x", "c", "d"]
        assert list(table[1]) == ["f", "d", "g"]
        assert list(table[2]) == ["i", "e", "g"]

    def test_table_sort_method_descending(self):
        table = Table(
            header=("A", "B", "C"),
            data=(("i", "e", "g"), ("x", "c", "d"), ("f", "d", "g")),
        )
        table.sort("B", asc=False)
        assert list(table[0]) == ["i", "e", "g"]
        assert list(table[1]) == ["f", "d", "g"]
        assert list(table[2]) == ["x", "c", "d"]

    def test_table_sorted_method(self):
        table = Table(header=("A", "B", "C"), data=((8, 5, 6), (9, 3, 4), (6, 4, 7)))
        sorted_table = table.sorted("B")
        assert list(sorted_table[0]) == [9, 3, 4]
        assert list(sorted_table[1]) == [6, 4, 7]
        assert list(sorted_table[2]) == [8, 5, 6]
        assert sorted_table is not table

    def test_table_split_by_row_count_method(self):
        table = Table(
            header=["A", "B", "C"],
            data=(
                (1, 2, 3),
                (4, 5, 6),
                (7, 8, 9),
                (10, 11, 12),
                (13, 14, 15),
                (15, 16, 17),
            ),
        )
        split_tables = table.split_by_row_count(2)
        assert len(split_tables) == 3
        for table in split_tables:
            assert len(table) == 2
        assert tuple(split_tables[0][0]) == (1, 2, 3)
        assert tuple(split_tables[0][1]) == (4, 5, 6)
        assert tuple(split_tables[1][0]) == (7, 8, 9)
        assert tuple(split_tables[1][1]) == (10, 11, 12)
        assert tuple(split_tables[2][0]) == (13, 14, 15)
        assert tuple(split_tables[2][1]) == (15, 16, 17)

    def test_table_split_by_row_count_method_with_odd_number_of_rows(self):
        table = Table(
            header=["A", "B", "C"],
            data=(
                (1, 2, 3),
                (4, 5, 6),
                (7, 8, 9),
                (10, 11, 12),
                (13, 14, 15),
                (15, 16, 17),
                (18, 19, 20),
            ),
        )
        split_tables = table.split_by_row_count(2)
        assert len(split_tables) == 4
        assert len(split_tables[0]) == 2
        assert tuple(split_tables[0][0]) == (1, 2, 3)
        assert tuple(split_tables[0][1]) == (4, 5, 6)
        assert len(split_tables[1]) == 2
        assert tuple(split_tables[1][0]) == (7, 8, 9)
        assert tuple(split_tables[1][1]) == (10, 11, 12)
        assert len(split_tables[2]) == 2
        assert tuple(split_tables[2][0]) == (13, 14, 15)
        assert tuple(split_tables[2][1]) == (15, 16, 17)
        assert len(split_tables[3]) == 1
        assert tuple(split_tables[3][0]) == (18, 19, 20)

    def test_table_append_method_with_iterable(self):
        table = TablerTestTools.basic_table()
        new_row = ("Pink", "Purple", "Brown")
        table.append(new_row)
        assert tuple(table[2]) == new_row

    def test_table_append_method_with_TableRow(self):
        table = TablerTestTools.basic_table()
        data = ("Pink", "Purple", "Brown")
        new_row = TableRow(data, TablerTestTools.TEST_HEADER)
        table.append(new_row)
        assert tuple(table[2]) == data

    def test_table_row__str__method(self):
        table = TablerTestTools.basic_table()
        row = table.rows[0]
        expected = "Red, Green, Blue"
        assert str(row) == expected

    def test_print_r_method(self, capsys):
        table = TablerTestTools.basic_table()
        table.print_r()
        captured = capsys.readouterr()
        assert (
            captured.err
            == "['Red', 'Green', 'Blue']\n['Orange', 'Yellow', 'Magenta']\n"
        )
