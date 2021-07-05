"""
This module provides the :class:`tabler.tabletypes.BaseTableType`.

This can be subclassed to provide Table Types for :class:`tabler.Table`.
They provide methods for opening and saving tables in different formats.
"""

from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Type, Union

from tabler import exceptions

if TYPE_CHECKING:
    from pathlib import Path

    from tabler import Table


def all_subclasses(cls: Type) -> List[Type]:
    """Return all subclasses of class recursivley.

    :param class cls: Class for which subclasses will be returned.
    :rtype: list(class)
    """
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in all_subclasses(s)
    ]


class BaseTableType:
    """Base class for Table Types.

    Table types are used to provide methods to :class:`tabler.Table` to load
    data from files and write to files of different types.

    Subclasses should implement :func:`tabler.tabletypes.BaseTableType.write`
    and / or :func:`tabler.tabletypes.BaseTableType.open` methods.

    Subclasses can also implement an **extensions** property. This is a list
    of file extensions matching the Table Type. It will then be used
    automatically when opening or writing files with a path ending in that
    extension if no table type is specified.

    Example::

        extensions = ['.csv', '.txt']
    """

    empty_value: Union[str, int, float, None] = None
    verbose: bool = True
    null_values: Tuple[Union[str, int, float, None], ...] = ("", None)

    def __init__(self, extension: str, verbose: Optional[bool] = None) -> None:
        """Construct :class:`tabler.tabletypes.BaseTableType`.

        :param str extension: File extension.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.extension = extension
        if verbose is not None:
            verbose = self.verbose

    @classmethod
    def get_by_extension(cls, extension: str) -> Any:
        """Get apropriate subclass of **BaseTableType** for file extension.

        Uses :func:`tabler.tabletypes.basetabletype.all_subclasses` to check
        all subclasses of 'tabler.tabletypes.BaseTableType' for a matching
        extension in it's **extensions** property.

        :param str extension: File extension for which to file TableType.
        :raises tabler.exceptions.ExtensionNotRecognised: If no
            **BaseTableType** subclass matching **extension** is found.
        """
        for table_type in all_subclasses(cls):
            if extension.lower() in table_type.extensions:
                return table_type()
        raise exceptions.ExtensionNotRecognised(extension)

    def open_path(self, path: str) -> Tuple[List[str], List[List[Any]]]:
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        raise NotImplementedError

    def write(self, table: "Table", path: Union[str, "Path"]) -> None:
        """Save data from :class:`tabler.Table` to file.

        :param table:"Table" to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        raise NotImplementedError

    def parse_row_data(
        self, rows: List[List[Any]]
    ) -> Tuple[List[str], List[List[Any]]]:
        """Return header and rows."""
        try:
            header = [_ for _ in rows[0]]
            data = [self.parse_row(row) for row in rows[1:]]
        except IndexError:
            raise ValueError("Input has no header or data.")
        return header, data

    def parse_value(self, value: Any) -> Any:
        """Return None if the value is empty, otherwise return str(value)."""
        if value in self.null_values:
            return self.empty_value
        else:
            return value

    def parse_row(self, row: List[Any]) -> List[Any]:
        """Return a row of parsed values."""
        return [self.parse_value(value) for value in row]

    def prepare_value(self, value: Any) -> Any:
        """Prepare a value for writing."""
        if value in self.null_values:
            return self.empty_value
        else:
            return value

    def prepare_row(
        self, row: List[Union[str, int, float, None]]
    ) -> List[Union[str, int, float, None]]:
        """Remove excess empty values."""
        while row[-1] == self.empty_value:
            row = row[:-1]
        return [self.prepare_value(value) for value in row]

    def prepare_rows(
        self,
        header: List[Any],
        rows: List[List[Any]],
    ) -> List[List[Any]]:
        """Prepare rows for writing."""
        data: List[List[Any]] = [header]
        data.extend([self.prepare_row(row) for row in rows])
        return data
