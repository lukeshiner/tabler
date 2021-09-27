"""This module provides Table Types for .csv files."""

import csv
import sys
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union

import requests

from .basetabletype import BaseTableType

if TYPE_CHECKING:
    from pathlib import Path

    from tabler.table import Table


class CSV(BaseTableType):
    """Table Type for comma separated value (.csv) files.

    :param str encoding: Encoding of file. Default: utf8.
    :param str delimiter: Delimiter used by file. Default , (Comma).
    :param str extension: Extension of file to save. Default .csv.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions = [".csv", ".txt"]
    empty_value = ""

    def __init__(
        self,
        encoding: str = "utf-8",
        delimiter: str = ",",
        extension: str = ".csv",
        verbose: Optional[bool] = None,
    ):
        """Consturct :class:`tabler.tabletypes.CSV`.

        :param str encoding: Encoding of file. Default: utf8.
        :param str delimiter: Delimiter used by file. Default , (Comma).
        :param str extension: Extension of file to save. Default .csv.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.encoding = encoding
        self.delimiter = delimiter
        super().__init__(extension, verbose=verbose)

    def open_path(self, path: str) -> Tuple[List[str], List[List[Any]]]:
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        with open(str(path), "r", encoding=self.encoding) as f:
            data = list(csv.reader(f, delimiter=self.delimiter))
        return self.parse_row_data(data)

    def write(self, table: "Table", path: Union[str, "Path"]) -> None:
        """Save data from :class:`tabler.Table` to file.

        :param table:"Table" to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        with open(str(path), "w", newline="", encoding=self.encoding) as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            if table.header:
                writer.writerow(table.header)
            for row in table:
                writer.writerow(list(row))
        print(
            "Written {} rows to file {}".format(len(table.rows), path), file=sys.stderr
        )

    def parse_value(self, value: Any) -> Any:
        """Return None if the value is empty, otherwise return str(value)."""
        value = super().parse_value(value)
        return str(value)


class CSVURL(CSV):
    """Table type for opening .csv files over HTTP."""

    def open_path(self, path: str) -> Tuple[List[str], List[List[Any]]]:
        """Return header and rows from file.

        :param str path: URL of file to be opened.
        """
        request = requests.get(path)
        text = []
        for line in request.iter_lines():
            text.append(line.decode(self.encoding))
        data = list(csv.reader(text))
        return self.parse_row_data(data)

    def write(self, table: "Table", path: Union[str, "Path"]) -> None:
        """Save data from :class:`tabler.Table` to file.

        :param table:"Table" to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        raise NotImplementedError
