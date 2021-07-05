"""This module provides a Table Type for Open Document Format (.ods) files."""

import sys
from typing import TYPE_CHECKING, Any, List, Tuple, Union

import pyexcel_ods3  # type: ignore

from .basetabletype import BaseTableType

if TYPE_CHECKING:
    from pathlib import Path

    from tabler.table import Table


class ODS(BaseTableType):
    """Table Type for Open Document Format (.ods) files.

    :param str extension: Extension of file to save. Default .ods.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions: List[str] = [".ods"]
    empty_value: Any = ""

    def __init__(self, sheet: int = 0, extension: str = ".ods", verbose: bool = True):
        """Consturct :class:`tabler.tabletypes.ODS`.

        :param str extension: Extension of file to save. Default .ods.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.sheet = sheet
        super().__init__(extension, verbose=verbose)

    def open_path(self, path: Union[str, "Path"]) -> Tuple[List[str], List[List[Any]]]:
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        data = pyexcel_ods3.get_data(str(path))
        sheet = data[list(data.keys())[self.sheet]]
        return self.parse_row_data(sheet)

    def write(self, table: "Table", path: Union[str, "Path"]) -> None:
        """Save data from :class:`tabler.Table` to file.

        :param table:"Table" to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        rows = self.prepare_rows(list(table.header), [list(_) for _ in table.rows])
        sheets = {"Sheet {}".format(self.sheet): rows}
        pyexcel_ods3.save_data(str(path), sheets)
        print(
            "Written {} rows to file {}".format(len(table.rows), path), file=sys.stderr
        )
