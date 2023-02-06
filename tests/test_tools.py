from pathlib import Path

from tabler import Table


class TablerTestTools:
    TEST_HEADER = ("Col1", "Col2", "Col3")
    TEST_ROW_1 = ["Red", "Green", "Blue"]
    TEST_ROW_2 = ["Orange", "Yellow", "Magenta"]
    TEST_DATA = [TEST_ROW_1, TEST_ROW_2]

    @classmethod
    def table_valid(cls, table):
        assert len(table.header) == 3
        assert len(table) == 2
        assert all([len(row) == 3 for row in table])
        assert table.header == cls.TEST_HEADER
        assert list(table.rows[0]) == cls.TEST_ROW_1
        assert list(table.rows[1]) == cls.TEST_ROW_2
        assert table[0]["Col1"] == "Red"

    @classmethod
    def basic_table(cls):
        header = cls.TEST_HEADER
        data = cls.TEST_DATA
        return Table(header=header, data=data)


class TableTypeTestTools:
    tabletype = None
    BASIC_FILE_PATH = None
    WITH_NULLS_PATH = None
    WITH_INCOMPLETE_ROW = None
    WITH_LONG_ROW = None

    @classmethod
    def open_with_table_type(cls, table_type, path):
        table = Table(path, table_type=table_type)
        TablerTestTools.table_valid(table)

    @classmethod
    def write_with_table_type(cls, table_type, tmpdir):
        out_table = TablerTestTools.basic_table()
        filepath = Path(str(tmpdir)) / "testfile{}".format(table_type.extension)
        out_table.write(filepath, table_type=table_type)
        in_table = Table(filepath, table_type=table_type)
        assert [list(_) for _ in in_table] == [list(_) for _ in out_table]

    @classmethod
    def read_null_values_with_tabletype(cls, table_type, path):
        table = Table(path, table_type=table_type)
        assert list(table[0]) == ["Red", table_type.empty_value, "Blue"]

    @classmethod
    def format_with_table_type(cls, table_type, path, expected_formatting):
        table = Table(path, table_type=table_type)
        assert list(table.get_column("Values")) == expected_formatting

    @classmethod
    def write_null_values_with_table_type(cls, table_type, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[
                ["Red", table_type.empty_value, "Blue"],
                ["Orange", "Yellow", "Magenta"],
            ],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=table_type)

    @classmethod
    def read_incomplete_rows_with_table_type(cls, table_type, path):
        table = Table(path, table_type)
        assert list(table[0]) == ["Red", "Green", table_type.empty_value]

    @classmethod
    def write_incomplete_rows_with_table_type(cls, table_type, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=table_type)

    @classmethod
    def read_long_rows_with_table_type(cls, table_type, path):
        table = Table(path, table_type)
        assert table.header == ("Col1", "Col2", "Col3", table._EMPTY_HEADER.format(1))
        assert list(table[0]) == ["Red", "Green", "Blue", "Purple"]

    @classmethod
    def write_long_rows_with_table_type(cls, table_type, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red", "Green", "Blue", "Purple"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=table_type)
