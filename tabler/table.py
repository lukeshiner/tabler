"""Table class.

This module provides the :class:`tabler.Table` class to read, write and edit
tabulated data.

"""

import os
import pathlib

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

    def __init__(
            self, filepath=None, table_type=None, header=None, data=None):
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

        :raises ValueError: If filepath is None or both header and data are
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
                        'Table Type not specified and extension {} '
                        'not recognised.'.format(extension))
            self.load(*self.table_type.open(filepath))
        elif isinstance(header, list) and isinstance(data, list):
            self.load(header, data)
        else:
            raise ValueError(
                'Either filepath or header and data must be specified')

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        for row in self.rows:
            yield row

    def __getitem__(self, index):
        return self.rows[index]

    def __str__(self):
        columns = str(len(self.columns))
        rows = str(len(self.rows))
        lines = [
            'Table Object containing {} colomuns and {} rows'.format(
                columns, rows),
            'Column Headings: {}'.format(', '.join(self.header))]
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def empty(self):
        """Clear all data."""
        self.rows = []
        self.header = []
        self.columns = []
        self.headers = {}

    def set_headers(self):
        """Create a lookup for header indexes."""
        self.headers = {}
        for column in self.header:
            self.headers[column] = self.header.index(column)

    def set_columns(self):
        """Create lookup to allow accessing table data by column."""
        self.columns = []
        column_number = 0
        for column in self.header:
            this_column = []
            row_number = 0
            for row in self.rows:
                this_column.append(self.rows[row_number].row[column_number])
                row_number += 1
            self.columns.append(this_column)
            column_number += 1

    def is_empty(self):
        """Return True if the table conatins no data, otherwise return False.

        :rtype: bool
        """
        if self.rows == []:
            if self.header == []:
                if self.columns == []:
                    return True
        return False

    def append(self, row):
        """Add new row to table.

        :param row: Data for new row.
        :type row: list or :class:`tabler.tablerow.TableRow`.
        """
        if isinstance(row, list):
            self.rows.append(TableRow(row, self.header))
            self.set_table()
        elif isinstance(row, TableRow):
            self.rows.append(row)

    def get_column(self, column):
        """Return all values in a column.

        :param column: Name or index of to be returned.
        :type column: str or int.
        :rtype: list
        """
        return self.columns[self.headers[column]]

    def remove_column(self, column):
        """
        Remove a specified column from the Table.

        :param column: Name or index of to be removed.
        :type column: str or int.
        """
        for row in self.rows:
            row.remove_column(column)
        self.set_headers()
        self.set_columns()

    def load(self, header, data):
        """
        Populate table with header and data.

        :param list header: Names of column headers.

        :param data: Rows of data. Each row must be a list of cell
            values
        :type data: list(list(str, int or float))
        """
        self.empty()
        self.header = [head for head in header]
        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow([cell for cell in row], header))
        self.set_table()

    def write(self, filepath, table_type=None):
        """Create file from table.

        :param table_type: Table Type to use to save the file.
        :type table_type: :class:`tabler.BaseTableType`

        :param str filepath: Path at which the file will be saved.
        """
        if not isinstance(filepath, pathlib.Path):
            filepath = pathlib.Path(filepath)
        if table_type is None:
            if self.table_type is not None:
                table_type = self.table_type
            else:
                table_type = BaseTableType.get_by_extension(filepath.suffix)
        if filepath.suffix != table_type.extension:
            filepath = pathlib.Path(str(filepath) + table_type.extension)
        table_type.write(self, filepath)

    def print_r(self):
        """Print table data in a readable format."""
        for row in self.rows:
            print(row.row)

    def copy(self):
        """Return duplicate Table object."""
        return self.__class__(
            header=self.header, data=[row.row for row in self.rows])

    def sort(self, sort_key, asc=True):
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
            self.rows.sort(key=lambda x: float(x.row[column]), reverse=not asc)
        except ValueError:
            self.rows.sort(key=lambda x: x.row[column], reverse=not asc)

    def sorted(self, sort_key, asc=True):
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

    def multi_sort_direction(self, sort_direction):
        """Convert sort direction into boolean.

        :param sort_direction: Sort direction to convert.
        :type param: str or bool.

        :rtype: bool. True if ascending, False if decending.
        """
        if type(sort_direction) == str:
            if sort_direction.upper() not in (
                    'A', 'ASC', 'ASCENDING', 'D', 'DESC', 'DESCENDING'):
                raise Exception(
                    "sort_direction must be one of 'A', 'ASC'," +
                    " 'ASCENDING', 'D', 'DESC', 'DESCENDING'")
        elif type(sort_direction) != bool:
            raise TypeError('sort_direction must be str or bool')
        if type(sort_direction) == str:
            if sort_direction in ('A', 'ASC', 'ASCENDING'):
                return True
            elif sort_direction in ('D', 'DESC', 'DESCENDING'):
                return False

    def multi_sorted(self, *sort_keys):
        """Return copy of self sorted by multiple keys.

        :param list(tuple) sort_keys: Keys to sort by.
        :rtype: :class:`tabler.Table`.
        """
        temp_table = self.copy()
        temp_table.multi_sort(*sort_keys)
        return temp_table

    def split_by_row_count(self, row_count):
        """Split table by row count.

        Create multiple :class:`tabler.Table` instances each with a subset of
        this one's data.

        :param int row_count: Number of rows in each Table.
        :rtype: list(:class:`tabler.Table`).
        """
        split_tables = []
        for i in range(0, len(self.rows), row_count):
            new_table = Table()
            new_table.header = self.header
            new_table.rows = self.rows[i:i + row_count]
            split_tables.append(new_table)
        return split_tables

    def set_table(self):
        """Set header and column lookups."""
        self.set_headers()
        self.set_columns()

    def multi_sort_validate(self, sort_key):
        """Validate sort key.

        :param sort_key: Sort key to validate.
        :type sort_key: int or str.

        :rtype: bool.
        """
        if type(sort_key) not in (int, str):
            raise TypeError('Sort Key must be of type int or str.')
        if sort_key not in self.header:
            raise KeyError('String Sort Key must be in header.')
        return True
