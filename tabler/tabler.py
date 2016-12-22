#!/usr/bin/python3

# tabulator by Luke Shiner (luke@lukeshiner.com)

import csv
import requests

from . tablerow import TableRow


class Tabler(object):
    """ Container for tabulated data. Can be created from a .csv by
    passing the file path to __init__.
    """
    def __init__(
            self, filename=None, header=None, data=None,
            encoding='utf-8', delimiter=','):
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
        total = str(len(self.columns) * len(self.rows))
        string = 'CsvFile Object containing ' + columns + ' colomuns and '
        string = string + rows + ' rows. ' + total + ' total entries.'
        return string

    def is_url(self, url):
        if url[0:7].lower() == 'http://':
            return True
        if url[0:8].lower() == 'https://':
            return True
        if url[0:6].lower() == 'ftp://':
            return True
        return False

    def parse_csv_file(self, csv_file):
        rows = []
        for row in csv_file:
            rows.append(row)
        return rows

    def open(self, filename, encoding=None, delimiter=None):
        """ Creates Table object from a .csv file. This file must be
        comma separated and utf-8 encoded. The first row must contain
        column headers.

        If the object already contains date it will be overwritten.
        """

        if self.is_url(filename):
            self.open_url(filename)
        elif filename.split('.')[-1].lower() == 'ods':
            self.open_ods(filename)
        else:
            self.open_csv(filename, encoding=encoding, delimiter=delimiter)

    def open_csv(self, filename, encoding=None, delimiter=None):
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

    def open_ods(self, filename, sheet=0):
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

    def open_url(self, url):
        request = requests.get(url)
        text = []
        for line in request.iter_lines():
            if len(line) > 0:
                text.append(line.decode(self.encoding))
        csv_file = csv.reader(text)
        rows = self.parse_csv_file(csv_file)
        self.load_file(rows)

    def load_file(self, rows):
        self.header = rows[0]
        for row in rows[1:]:
            self.rows.append(TableRow(row, self.header))
        self.set_table()

    def load_from_database_table(self, database_table):
        """ Loads data from a MySQL table contained in a DatabaseTable
        object.
        """
        self.empty()
        self.header = database_table.get_columns()
        data = database_table.get_all()
        for row in data:
            self.rows.append(TableRow(row, self.header))

        self.set_table()

    def empty(self):
        """ Clears all data from the Table. The same as initialising a
        new Table with no arguments.
        """

        self.rows = []
        self.header = []
        self.columns = []
        self.headers = {}

    def set_headers(self):
        """ Creates a dictionary of headers for looking up the
        apropriate index in self.columns.
        """

        self.headers = {}
        for column in self.header:
            self.headers[column] = self.header.index(column)

    def set_columns(self):
        """ Creates a 2d list pivoted from self.rows.  """
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

    def set_table(self):
        self.set_headers()
        self.set_columns()

    def is_empty(self):
        """ Returns True if the table conatins no data, otherwise
        returns False.
        """
        if self.rows == []:
            if self.header == []:
                if self.columns == []:
                    return True
        return False

    def append(self, row):
        """ Creates a new row in the Table from a TableRow object or
        creates one from a list object with the correct number of
        values.
        """
        if isinstance(row, list):
            self.rows.append(TableRow(row, self.header))
            self.set_table()
        elif isinstance(row, TableRow):
            self.rows.append(row)

    def get_column(self, column):
        """ Returns a list containing all values from the specified
        column.
        """

        return self.columns[self.headers[column]]

    def remove_column(self, column):
        """ Removes a specified column from the Table.  """
        if column in self.header:
            for row in self.rows:
                row.remove_column(column)
            self.set_headers()
            self.set_columns()
            print('DELETED column: ' + column)
        else:
            return False

    def getRows(self):
        return self.rows

    def load_from_array(self, data, header):
        """ Loads the Table with data contained in a 2d list
        object.
        """

        self.empty()
        self.header = header
        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow(row, header))
        self.set_table()

    def write_csv(self, filename, header=True, encoding=None, delimiter=None):
        """ Creates a .csv of the data contained within the Table with
        the specifed filename or filepath.
        This file will be comma separated and UTF-8 encoded.
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
        from collections import OrderedDict
        from pyexcel_ods3 import save_data
        data = OrderedDict()
        sheet = [self.header]
        sheet += self.rows
        data.update({"Sheet 1": sheet})
        save_data(filename, data)
        print('Writen ' + str(len(self.rows)) + ' lines to file ' + filename)

    def to_html(self, header=True):
        """ Returns a string containg the data held in the Table as
        as html table.
        If header=True the column headings will be included in <th>
        tags. If it is False no headings will be written.
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
        html_file = open(filename, 'w', encoding='utf-8')
        html_file.write(self.to_html(header=header))
        html_file.close()

    def print_r(self):
        for row in self.rows:
            print(row.row)

    def copy(self):
        new_table = Tabler()
        new_table.header = self.header
        for row in self.rows:
            new_table.rows.append(row.copy())
        new_table.set_table()
        return new_table

    def sort(self, sort_key, asc=True):
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
        temp_table = self.copy()
        temp_table.sort(sort_key, asc)
        return temp_table

    def multi_sort_direction(self, sort_direction):
        if type(sort_direction) == str:
            if sort_direction.upper() not in ('A', 'ASC', 'ASCENDING',
                                              'D', 'DESC',
                                              'DESCENDING'):
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

    def multi_sort_validate(self, sort_key):
        if type(sort_key) not in (int, str):
            raise TypeError('sort_key Must be int')
        if sort_key not in self.header:
            raise KeyError('sort_key must be in header')
        return True

    def multi_sort(self, *sort_keys):
        if type(sort_keys) in (list, tuple):
            if type(sort_keys[0]) in (list, tuple):
                sort_keys = reversed(sort_keys)
        for sort_pair in sort_keys:
            if type(sort_pair) in (str, int):
                sort_key = sort_pair
            elif type(sort_pair) in (list, tuple):
                sort_key, sort_direction = sort_pair
            else:
                raise TypeError(
                    'sort_keys must be int, str, list or tuple. Not ' +
                    str(type(sort_pair)))
            if self.multi_sort_validate(sort_key):
                asc = self.multi_sort_direction(sort_direction)
                self.sort(sort_key, asc)

    def multi_sorted(self, *sort_keys):
        temp_table = self.copy()
        temp_table.multi_sort(*sort_keys)
        return temp_table

    def split_by_row_count(self, row_count):
        split_tables = []
        for i in range(0, len(self.rows), row_count):
            new_table = Tabler()
            new_table.header = self.header
            new_table.rows = self.rows[i:i + row_count]
            split_tables.append(new_table)
        return split_tables
