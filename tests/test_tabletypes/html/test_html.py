from pathlib import Path

import pytest

from tabler import HTML, Table

from ...test_tools import TablerTestTools


class TestHTML:
    def test_open(self):
        with pytest.raises(NotImplementedError):
            Table("", table_type=HTML())

    def test_write(self, tmpdir):
        table = TablerTestTools.basic_table()
        filepath = str(Path(str(tmpdir)) / "testfile.html")
        table.write(filepath, table_type=HTML())
        with open(str(Path(__file__).parent / "expected.html"), "r") as f:
            expected = f.read()
        with open(filepath, "r") as f:
            assert f.read() == expected
