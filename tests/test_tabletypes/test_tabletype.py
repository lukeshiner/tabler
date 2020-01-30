import pytest

from tabler.tabletypes.basetabletype import BaseTableType

from ..test_tools import TablerTestTools


class TestBaseTableType:
    def test_prepare_row(self):
        table_type = BaseTableType(".csv")
        table_type.empty_value = None
        row = [1, 3, "A", None, 5, "C", None, None, None]
        prepared_row = table_type.prepare_row(row)
        assert list(prepared_row) == [1, 3, "A", None, 5, "C"]

    def test_open(self):
        table_type = BaseTableType(".csv")
        with pytest.raises(NotImplementedError):
            table_type.open_path("path")

    def test_write(self):
        table_type = BaseTableType(".csv")
        with pytest.raises(NotImplementedError):
            table_type.write(TablerTestTools.basic_table(), "path")
