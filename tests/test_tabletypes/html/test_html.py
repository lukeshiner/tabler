from pathlib import Path

import pytest

from tabler import HTML, Table

from ..test_tabletype import TableTypeTest


class TestHTML(TableTypeTest):
    tabletype = HTML()

    def test_open(self):
        with pytest.raises(NotImplementedError):
            Table("", table_type=HTML())

    def test_write(self, tmpdir):
        table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile.html"
        table.write(filepath, table_type=HTML())

    def test_read_null_values(self):
        pass

    def test_read_incomplete_rows(self):
        pass

    def test_read_long_rows(self):
        pass
