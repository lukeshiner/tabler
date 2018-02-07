"""This module provides a Table Type for Open Document Format (.ods) files."""

from collections import OrderedDict

import ezodf
from pyexcel_ods3 import save_data

from .basetabletype import BaseTableType


class ODS(BaseTableType):
    """Table Type for Open Document Format (.ods) files.

    :param str extension: Extension of file to save. Default .ods.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions = ['.ods']

    def __init__(self, sheet=0, extension='.ods', verbose=True):
        """Consturct :class:`tabler.tabletypes.ODS`.

        :param str extension: Extension of file to save. Default .ods.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.sheet = sheet
        super().__init__(extension, verbose=verbose)

    def open(self, path):
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        doc = ezodf.opendoc(path)
        sheet = doc.sheets[self.sheet]
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
        return rows[0], rows[1:]

    def write(self, table, path):
        """Save data from :class:`tabler.Table` to file.

        :param table: Table to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        data = OrderedDict()
        sheet = [table.header]
        sheet += table.rows
        data.update({"Sheet 1": sheet})
        save_data(str(path), data)
        print('Written {} rows to file {}'.format(len(table.rows), path))
