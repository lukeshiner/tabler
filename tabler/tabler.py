# -*- coding: utf-8 -*-

"""
Table.Table
~~~~~~~~~~~~~

This module provides a Table object to read, write and edit tabulated
data.

"""

import csv
import requests

from . tablerow import TableRow


class Tabler(object):

    """A Table table.

    A wrapper object for tabulated data.

    """

    def __init__(
            self, filename=None, header=None, data=None,
            encoding='utf-8', delimiter=','):
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
        self.empty()
        self.encoding = encoding
        self.delimiter = delimiter
        if isinstance(filename, str):
            self.open(filename)
        if isinstance(header, list):
            self.header = header
        if isinstance(data, list):
            self.load_from_array(data, self.header)

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

    def open_csv(self, filename, encoding=None, delimiter=None):
        """Create Table object from a .csv file.

        This file must be in comma separated format. The first row is assumed
        to contain column headers.

        If the object already contains data it will be overwritten.

        :param filename: :string: Relative or absolute path to .ods file from
            which data will be loaded.

        :param encoding: (optional) Encoding of file to be loaded. (Default:
            self.encoding)

        :rtype: tabler.Table
        """
        if encoding is None:
            encoding = self.encoding
        if delimiter is None:
            delimiter = self.delimiter
        open_file = open(
            filename, 'rU', encoding=self.encoding, errors='replace',)
        csv_file = csv.reader(open_file, delimiter=delimiter)
        rows = self.parse_csv_file(csv_file)
        self.load_file(rows)
        open_file.close()
        return self

    def open_ods(self, filename, sheet=0):
        """Load data from a .ods Open Document Format Spreadsheet.

        As only one sheet can be loaded at a time, the sheet kwarg can be used
        to specify which sheet will be loaded.

        :param filename: :string: Relative or absolute path to .ods file from
            which data will be loaded.

        :param sheet: (optional) Index of sheet in .ods file to be loaded.
            (Default: 0)

        :rtype: tabler.Table
        """
        import ezodf
        doc = ezodf.opendoc(filename)
        sheet = doc.sheets[sheet]
        rows = []
        for row in sheet:
            new_row = []
            for cell in row:
                if cell.value is not None:
                    new_row.append(cell.value)
                else:
                    new_row.append('')
            if len(row) > 0:
                rows.append(new_row)
        self.load_file(rows)
        return self

    def open_url(self, url):
        """Load data from a .csv file located at the passed URL.

        :param url: URL from which data will be loaded.

        :rtype: tabler.Table
        """
        request = requests.get(url)
        text = []
        for line in request.iter_lines():
            if len(line) > 0:
                text.append(line.decode(self.encoding))
        csv_file = csv.reader(text)
        rows = self.parse_csv_file(csv_file)
        self.load_file(rows)
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

    def load_from_list(self, data, header):
        """
        Load the Table with data contained in a 'list' (column) of
        `lists` (rows).

        :param data: `list` of rows to be added to Table.

        :param header: 'list' containing column headers for data. Order
            is important.

        :rtype: tabler.Table
        """
        self.empty()
        self.header = header
        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow(row, header))
        self.set_table()
        return self

    def write_csv(self, filename, header=True, encoding=None, delimiter=None):
        """Create a .csv formatted file from the data contained within the
        table at the absolute or relative path filename.
        This file will be comma separated.

        :param filename: Absolute or relative path at which to create the file.

        :param encoding: (Optional) Encoding for file to be written.
            (Default: self.encoding)
        """

        if encoding is None:
            encoding = self.encoding
        if delimiter is None:
            delimiter = self.delimiter
        csv_file = open(filename, 'w', newline='', encoding=encoding)
        writer = csv.writer(csv_file, delimiter=delimiter)
        if header is True:
            writer.writerow(self.header)
        for row in self:
            writer.writerow(row.to_array())
        csv_file.close()
        print('Writen ' + str(len(self.rows)) + ' lines to file ' + filename)

    def write(self, filename, header=True, encoding=None, delimiter=None):
        self.write_csv(
            filename, header=header, encoding=encoding, delimiter=delimiter)

    def write_ods(self, filename):
        """Write data in Open Document Spreadsheet (.ods) format.

        :param filename: Absolute or relative path at which to create the file.
        """
        from collections import OrderedDict
        from pyexcel_ods3 import save_data
        data = OrderedDict()
        sheet = [self.header]
        sheet += self.rows
        data.update({"Sheet 1": sheet})
        save_data(filename, data)
        print('Writen ' + str(len(self.rows)) + ' lines to file ' + filename)

    def to_html(self, header=True):
        """Create a string containg the data held in the Table as
        an HTML table.

        :param header: (Optional) If True HTML table will include column
            headers. If False they will be omitted.

        :rtype: str
        """
        open_table = '<table>\n'
        close_table = '</table>\n'
        open_tr = '\t<tr>\n'
        close_tr = '\t</tr>\n'
        open_th = '\t\t<th>'
        close_th = '</th>\n'
        open_td = '\t\t<td>'
        close_td = '</td>\n'
        html_table = ''
        html_table += open_table
        if header:
            html_table += open_tr
            for head in self.header:
                html_table += open_th
                html_table += str(head)
                html_table += close_th
            html_table += close_tr
        for row in self.rows:
            html_table += open_tr
            for cell in row:
                html_table += open_td
                html_table += str(cell)
                html_table += close_td
            html_table += close_tr
        html_table += close_table
        return html_table

    def to_html_file(self, filename, header=True):
        """Write table as HTML to file.

        :param filename: Absolute or relative path at which the file will be
            written.

        :param header: (Optional) If True HTML table will include column
            headers. If False they will be omitted.
        """
        html_file = open(filename, 'w', encoding='utf-8')
        html_file.write(self.to_html(header=header))
        html_file.close()

    def print_r(self):
        """Print Table data in a readable format.
        """
        for row in self.rows:
            print(row.row)

    def copy(self):
        """Return duplicate Table object. This Table will can be edited
        separatly from this one.
        """
        new_table = Tabler()
        new_table.header = self.header
        for row in self.rows:
            new_table.rows.append(row.copy())
        new_table.set_table()
        return new_table

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
            new_table = Tabler()
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

    def getRows(self):
        return self.rows

    def parse_csv_file(self, csv_file):
        rows = []
        for row in csv_file:
            rows.append(row)
        return rows

    def multi_sort_validate(self, sort_key):
        if type(sort_key) not in (int, str):
            raise TypeError('sort_key Must be int')
        if sort_key not in self.header:
            raise KeyError('sort_key must be in header')
        return True

    def is_url(self, url):
        if url[0:7].lower() == 'http://':
            return True
        if url[0:8].lower() == 'https://':
            return True
        if url[0:6].lower() == 'ftp://':
            return True
        return False
