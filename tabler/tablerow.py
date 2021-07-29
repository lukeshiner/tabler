"""Provides the TableRow class.

TableRow provides methods for working with rows in :class:`tabler.Table`
instances.
"""

from typing import Any, Iterable, Iterator, List, Union


class TableRow:
    """Provide methods for rows in :class:`tabler.Table` instances."""

    def __init__(self, row: List[List[Any]], header: Iterable[str]):
        """Instansiate :class:`TableRow`.

        :param list row: Data stored in this row.
        :param list header: Column headers from table.
        """
        self.row = row
        self.header = tuple(header)
        self.headers = {}

        for column in self.header:
            self.headers[column] = self.header.index(column)

    def __iter__(self) -> Iterator:
        for item in self.row:
            yield item

    def __getitem__(self, index: Union[int, str]) -> Any:
        if isinstance(index, int):
            return self.row[index]
        elif isinstance(index, str):
            return self.row[self.headers[index]]
        else:
            raise ValueError(f"Index must be int or str, not {type(index)}.")

    def __setitem__(self, index: Union[str, int], item: Any) -> None:
        if isinstance(index, int):
            self.row[index] = item
        elif isinstance(index, str):
            self.row[self.headers[index]] = item
        else:
            raise ValueError(f"Index is must be int or str, not {type(index)}.")

    def __str__(self) -> str:
        return ", ".join((str(cell) for cell in self.row))

    def __len__(self) -> int:
        return len(self.row)

    def remove_column(self, column: str) -> None:
        """Remove the passed column.

        :param str column: Header for column to be removed.
        :raises: ValueError: If column is not a valid column header.
        """
        column_index = self.header.index(column)
        self.row.pop(column_index)
        header = list(self.header)
        header.pop(header.index(column))
        self.header = tuple(header)

    def copy(self) -> "TableRow":
        """Return duplicate tabler.tablerow.TableRow object.

        :rtype: :class:`tabler.tablerow.TableRow`.
        """
        return TableRow(self.row, self.header)
