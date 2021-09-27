"""
Table class.

This module provides the :class:`tabler.Table` class to read, write and edit
tabulated data.

"""

import os
import pathlib
import sys
from pathlib import Path
from typing import Any, Collection, Iterable, Iterator, List, Optional, Tuple, Union

from . import exceptions
from .tablerow import TableRow
from .tabletypes import BaseTableType


class Table:
    """A wrapper object for tabulated data.

    Allows access to and manipulation of tablulated data. This data can be
    input directly or loaded from a file. Data can also be writen data to a
    file. Table rows are encapsulated with the
    :class:`tabler.tablerow.TableRow` class.

    Different filetypes can be read and written by providing a subclass of
    :class:`tabler.tabletypes.BaseTableType` which implements the open and
    write methods.

    A `filename` can be provided to open an existing file. An apropriate
    :class:`tabler.tabletypes.BaseTableType` object can be provided to specify
    how the file will be opened. If this is not specified one will be selected
    based on the file extension in the `filename` using default parameters.

    Alternatively **header** and **data** can be specified to populate the
    table directly.

    :param table_type: Table Type to use to open a file referenced
        by `filetype`.
    :type table_type: :class:`tabler.tabletypes.BaseTableType`

    :param str filepath: Path to file to be opened.

    :param list header: List of column headers to be used if not loaded
        from file.

    :param data: Two dimensional list. Each list will form a row of cell
        data.
    :type data: list(list(str, int or float))

    :raises ValueError: If filepath is None or both header and data are
        None.
    """

    _EMPTY_HEADER = "Unlabeled Column {}"

    def __init__(
        self,
        filepath: Optional[str] = None,
        table_type: Optional[BaseTableType] = None,
        header: Optional[Collection[str]] = None,
        data: Optional[Iterable] = None,
    ) -> None:
        """Construct a :class:`tabler.Table`.

        A `filename` can be provided to open an existing file. An apropriate
        :class:`tabler.tabletypes.BaseTableType` object can be provided to
        specify how the file will be opened. If this is not specified one will
        be selected based on the file extension in the `filename` using
        default parameters.

        Alternatively **header** and **data** can be specified to populate the
        table directly.

        :param table_type: Table Type to use to open a file referenced
            by `filetype`.
        :type table_type: :class:`tabler.tabletypes.BaseTableType`

        :param str filepath: Path to file to be opened.

        :param list header: List of column headers to be used if not loaded
            from file.

        :param data: Two dimensional list. Each list will form a row of cell
            data.
        :type data: list(list(str, int or float))

        :raises TypeError: If filepath is None or both header and data are
            None.
        """
        self.table_type = table_type
        if filepath is not None:
            if self.table_type is None:
                extension = os.path.splitext(filepath)[-1]
                try:
                    self.table_type = BaseTableType.get_by_extension(extension)
                except exceptions.ExtensionNotRecognised:
                    raise ValueError(
                        "Table Type not specified and extension {} "
                        "not recognised.".format(extension)
                    )
            self.load(*self.table_type.open_path(filepath))
        elif header is not None and data is not None:
            self.load(header, data)
        else:
            raise exceptions.TableInitialisationError()

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[TableRow]:
        for row in self.rows:
            yield row

    def __getitem__(self, index: int) -> TableRow:
        return self.rows[index]

    def __str__(self) -> str:
        columns = str(len(self.header))
        rows = str(len(self.rows))
        lines = [
            "Table Object containing {} colomuns and {} rows".format(columns, rows),
            "Column Headings: {}".format(", ".join(self.header)),
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    def load(
        self, header: Collection, data: Iterable[Union[Iterable, TableRow]]
    ) -> None:
        """
        Populate table with header and data.

        :param list header: Names of column headers.

        :param data: Rows of data. Each row must be a list of cell
            values
        :type data: list(list(str, int or float))
        """
        self.empty()
        self.row_length: int = max([len(header)] + [len(_) for _ in data])
        self.header: tuple = self._prepare_header(header)
        self.rows: List[TableRow] = [
            TableRow(row, self.header) for row in self._prepare_data(data)
        ]

    def write(
        self, filepath: Union[str, Path], table_type: Optional[BaseTableType] = None
    ) -> None:
        """Create file from table.

        :param table_type: Table Type to use to save the file.
        :type table_type: :class:`tabler.BaseTableType`

        :param str filepath: Path at which the file will be saved.
        """
        path = pathlib.Path(filepath)
        if table_type is None:
            if self.table_type is not None:
                table_type = self.table_type
            else:
                table_type = BaseTableType.get_by_extension(path.suffix)
        if path.suffix != table_type.extension:
            path = path.with_suffix(table_type.extension)
        table_type.write(self, path)

    def empty(self) -> None:
        """Clear all data."""
        self.rows = []
        self.header = ()

    def is_empty(self) -> bool:
        """Return True if the table conatins no data, otherwise return False.

        :rtype: bool
        """
        if len(self.rows) == 0 and len(self.header) == 0:
            return True
        return False

    def append(self, row: Union[Iterable, TableRow]) -> None:
        """Add new row to table.

        :param row: Data for new row.
        :type row: list or :class:`tabler.tablerow.TableRow`.
        """
        self.rows.append(TableRow(list(row), self.header))

    def get_column(self, column: Union[int, str]) -> List:
        """Return all values in a column.

        :param column: Name or index of to be returned.
        :type column: str or int.
        :rtype: list
        """
        return [row[column] for row in self.rows]

    def remove_column(self, column: str) -> None:
        """
        Remove a specified column from the Table.

        :param column: Name or index of to be removed.
        :type column: str or int.
        """
        header = list(self.header)
        header.pop(header.index(column))
        self.header = tuple(header)
        for row in self.rows:
            row.remove_column(column)

    def print_r(self) -> None:
        """Print table data in a readable format."""
        for row in self.rows:
            print(list(row), file=sys.stderr)

    def copy(self) -> "Table":
        """Return duplicate Table object."""
        return self.__class__(
            header=self.header, data=[row.copy() for row in self.rows]
        )

    def sort(self, sort_key: str, asc: bool = True) -> None:
        """Sort table by column.

        :param sort_key: Column header or index of column to sort by.
        :type sort_key: str or int

        :param bool asc: If True Table will be sorted in ascending order.
            Otherwise order will be descending. (Default: True)
        """
        if isinstance(sort_key, str):
            column = self.header.index(sort_key)
        else:
            column = sort_key
        try:
            self.rows.sort(key=lambda x: float(list(x)[column]), reverse=not asc)
        except ValueError:
            # https://github.com/python/mypy/issues/9656
            self.rows.sort(key=lambda x: list(x)[column], reverse=not asc)  # type: ignore

    def sorted(self, sort_key: str, asc: bool = True) -> "Table":
        """Return a sorted duplicate of the Table.

        :param sort_key: Column header or index of column to sort by.
        :type sort_key: str or int

        :param bool asc: If True Table will be sorted in ascending order.
            Otherwise order will be descending. (Default: True)

        :rtype: :class:`tabler.Table`.
        """
        temp_table = self.copy()
        temp_table.sort(sort_key, asc)
        return temp_table

    def split_by_row_count(self, row_count: int) -> List["Table"]:
        """Split table by row count.

        Create multiple :class:`tabler.Table` instances each with a subset of
        this one's data.

        :param int row_count: Number of rows in each Table.
        :rtype: list(:class:`tabler.Table`).
        """
        split_tables = []
        for i in range(0, len(self.rows), row_count):
            new_table = Table(header=self.header, data=self.rows[i : i + row_count])
            split_tables.append(new_table)
        return split_tables

    def _prepare_header(self, header_row: Iterable[str]) -> Tuple[str, ...]:
        unlabled = 0
        header = []
        for item in header_row:
            if not item:
                unlabled += 1
                header.append(self._EMPTY_HEADER.format(unlabled))
            else:
                header.append(item)
        while len(header) < self.row_length:
            unlabled += 1
            header.append(self._EMPTY_HEADER.format(unlabled))
        return tuple(header)

    def _prepare_data(
        self, data: Iterable, empty_value: Optional[Any] = None
    ) -> List[List[Any]]:
        return [self._prepare_row(row, empty_value=empty_value) for row in data]

    def _prepare_row(
        self, row: Iterable, empty_value: Optional[Any] = None
    ) -> List[Union[str, int, float, None]]:
        if empty_value is None and self.table_type is not None:
            empty_value = self.table_type.empty_value
        prepared_row = []
        for value in row:
            if value is None or value == "":
                prepared_row.append(empty_value)
            else:
                prepared_row.append(value)
        while len(prepared_row) < self.row_length:
            prepared_row.append(empty_value)
        return prepared_row
