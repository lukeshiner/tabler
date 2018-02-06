# -*- coding: utf-8 -*-

"""
Table.Table
~~~~~~~~~~~~~

This module provides a Table object to read, write and edit tabulated
data.

"""

import os
import pathlib

from . import exceptions
from .tablerow import TableRow
from .tabletype import TableType


class Table:

    """A Table table.

    A wrapper object for tabulated data.

    """

    def __init__(
            self, filepath=None, table_type=None, header=None, data=None):
        """Constructs a :class: `Table`.
        Returns :class: 'Table' object.

        :param filename: (Optional) URL, relative path or absolute path
            to `.csv` file or absolute or relative path to `.ods` file to
            be loaded.

        :param header: (Optional) List of column headers to be used if not
            loaded from file.

        :param data: (Optional) List of rows in the form of Lists of cell data
            to be loaded into the Table.

        :param encoding: Encoding to be used when reading or writing files.
            (Default 'utf-8')

        :rtype: tabler.Table
        """
        self.table_type = table_type
        if filepath is not None:
            if not isinstance(filepath, pathlib.Path):
                filepath = pathlib.Path(filepath)
            if self.table_type is None:
                extension = os.path.splitext(filepath)[-1]
                try:
                    self.table_type = TableType.get_by_extension(extension)
                except exceptions.ExtensionNotRecognised:
                    raise Exception(
                        'Table Type not specified and extension {} '
                        'not recognised.'.format(extension))
            self.load(*self.table_type.open(filepath))
        elif isinstance(header, list) and isinstance(data, list):
            self.load(header, data)
        else:
            raise Exception(
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
            'CsvFile Object containing {} colomuns and {} rows'.format(
                columns, rows),
            'Column Headings: {}'.format(', '.join(self.header))]
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def open(self, filename, encoding=None, delimiter=None):
        """ Creates Table object from a .csv file. This file must be
        comma separated and utf-8 encoded. The first row must contain
        column headers.

        If filename is URL formatted load from URL
        If filename extension is .ods load .ods
        Otherwise load .csv

        :param filename: :string: URL, relative or absolute path to .ods file
            from which data will be loaded.

        :param encoding: (optional) Encoding of file to be loaded. (Default:
            self.encoding)

        :rtype: tabler.Table
        """
        if self.is_url(filename):
            self.open_url(filename)
        elif filename.split('.')[-1].lower() == 'ods':
            self.open_ods(filename)
        else:
            self.open_csv(filename)
        return self

    def empty(self):
        """Clear all data from Table.

        :rtype: tabler.Table
        """
        self.rows = []
        self.header = []
        self.columns = []
        self.headers = {}
        return self

    def set_headers(self):
        """Create a `dictionary` of headers for looking up the apropriate index
        in self.columns.
        """
        self.headers = {}
        for column in self.header:
            self.headers[column] = self.header.index(column)

    def set_columns(self):
        """Create `Table.columns` to allow data to be accessed by column rather
        than row.
        """
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
        """Create a new row in the Table from a list with the correct number
        of values.

        Can also take rows from another Table object.

        :param row: `list` or `tabler.TableRow` object containig one row of
            data for the table.
        """
        if isinstance(row, list):
            self.rows.append(TableRow(row, self.header))
            self.set_table()
        elif isinstance(row, TableRow):
            self.rows.append(row)

    def get_column(self, column):
        """Return a `list` containing all values from the specified
        column.

        :param column: `string` column name or `int` index of column to
            be returned.
        """
        return self.columns[self.headers[column]]

    def remove_column(self, column):
        """
        Remove a specified column from the Table.

        :param column: `string` column name or `int` index of column to
            be removed.
        """
        if column in self.header:
            for row in self.rows:
                row.remove_column(column)
            self.set_headers()
            self.set_columns()
            print('DELETED column: ' + column)
        else:
            return False

    def load(self, header, data):
        """
        Create table with header and data.

        :param list header: Names of column headers.

        :param data: Rows of data. Each row must be a list of cell
            values
        """
        self.empty()
        self.header = header
        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow(row, header))
        self.set_table()

    def write(self, filepath, table_type=None):
        if not isinstance(filepath, pathlib.Path):
            filepath = pathlib.Path(filepath)
        if table_type is None:
            if self.table_type is not None:
                table_type = self.table_type
            else:
                table_type = TableType.get_by_extension(filepath.suffix)
        if filepath.suffix != table_type.extension:
            filepath = pathlib.Path(str(filepath) + table_type.extension)
        table_type.write(self, filepath)

    def print_r(self):
        """Print Table data in a readable format."""
        for row in self.rows:
            print(row.row)

    def copy(self):
        """Create duplicate Table object."""
        return self.__class__(
            header=self.header, data=[row.row for row in self.rows])

    def sort(self, sort_key, asc=True):
        """Sort table by column.

        :param sort_key: `string` column header or `int` index of column to
            sort by (`Table.column[sort_key]`).

        :param asc: If True Table will be sorted by `Table.column[sort_key]`
            in ascending order. If False order will be descending.
            (Default: True)
        """
        if type(sort_key) == str:
            if sort_key in self.header:
                column = self.header.index(sort_key)
            else:
                raise KeyError('sort_key must be int or in header')
        else:
            column = sort_key
        try:
            self.rows.sort(key=lambda x: float(x.row[column]), reverse=not asc)
        except ValueError:
            self.rows.sort(key=lambda x: x.row[column], reverse=not asc)

    def sorted(self, sort_key, asc=True):
        """Return a sorted duplicate of the Table.
        """
        temp_table = self.copy()
        temp_table.sort(sort_key, asc)
        return temp_table

    def multi_sort_direction(self, sort_direction):
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
        temp_table = self.copy()
        temp_table.multi_sort(*sort_keys)
        return temp_table

    def split_by_row_count(self, row_count):
        """Return `list` of Tables containing part of the data in self.
        These tables will contain a maximum number of rows specified in
        row_count.

        :param row_count: Maximum number of rows in each Table.
        """
        split_tables = []
        for i in range(0, len(self.rows), row_count):
            new_table = Table()
            new_table.header = self.header
            new_table.rows = self.rows[i:i + row_count]
            split_tables.append(new_table)
        return split_tables

    def set_table(self):
        self.set_headers()
        self.set_columns()

    def load_file(self, rows):
        self.header = rows[0]
        for row in rows[1:]:
            self.rows.append(TableRow(row, self.header))
        self.set_table()

    def parse_csv_file(self, csv_file):
        rows = []
        for row in csv_file:
            rows.append(row)
        return rows

    def multi_sort_validate(self, sort_key):
        if type(sort_key) not in (int, str):
            raise TypeError('Sort Key must be of type int.')
        if sort_key not in self.header:
            raise KeyError('Sort Key must be in header.')
        return True
