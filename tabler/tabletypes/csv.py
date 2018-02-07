"""This module provides Table Types for .csv files."""

import csv

import requests

from .basetabletype import BaseTableType


class CSV(BaseTableType):
    """Table Type for comma separated value (.csv) files.

    :param str encoding: Encoding of file. Default: utf8.
    :param str delimiter: Delimiter used by file. Default , (Comma).
    :param str extension: Extension of file to save. Default .csv.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions = ['.csv', '.txt']

    def __init__(
            self, encoding='utf-8', delimiter=',', extension='.csv',
            verbose=None):
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

    def open(self, path):
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        open_file = open(path, 'rU', encoding=self.encoding)
        csv_file = csv.reader(open_file, delimiter=self.delimiter)
        rows = [row for row in csv_file]
        return rows[0], rows[1:]

    def write(self, table, path):
        """Save data from :class:`tabler.Table` to file.

        :param table: Table to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        csv_file = open(path, 'w', newline='', encoding=self.encoding)
        writer = csv.writer(csv_file, delimiter=self.delimiter)
        if table.header:
            writer.writerow(table.header)
        for row in table:
            writer.writerow(row.row)
        csv_file.close()
        print('Written {} rows to file {}'.format(len(table.rows), path))


class CSVURL(CSV):
    """Table type for opening .csv files over HTTP."""

    def open(self, path):
        """Return header and rows from file.

        :param str path: URL of file to be opened.
        """
        request = requests.get(path)
        text = []
        for line in request.iter_lines():
            if len(line) > 0:
                text.append(line.decode(self.encoding))
        csv_file = csv.reader(text)
        rows = [row for row in csv_file]
        return rows[0], rows[1:]
