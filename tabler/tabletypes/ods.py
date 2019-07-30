"""This module provides a Table Type for Open Document Format (.ods) files."""

import sys

import odswriter
import pyexcel_ods

from .basetabletype import BaseTableType


class ODS(BaseTableType):
    """Table Type for Open Document Format (.ods) files.

    :param str extension: Extension of file to save. Default .ods.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions = [".ods"]

    def __init__(self, sheet=0, extension=".ods", verbose=True):
        """Consturct :class:`tabler.tabletypes.ODS`.

        :param str extension: Extension of file to save. Default .ods.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.sheet = sheet
        super().__init__(extension, verbose=verbose)

    def open_path(self, path):
        """Return header and rows from file.

        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        data = pyexcel_ods.get_data(str(path))
        sheet = data[list(data.keys())[0]]
        return sheet[0], sheet[1:]

    def write(self, table, path):
        """Save data from :class:`tabler.Table` to file.

        :param table: Table to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        with open(str(path), "wb") as f:
            with odswriter.writer(f) as odsfile:
                for row in table:
                    odsfile.writerow(table.header)
                    odsfile.writerow(row)
        print(
            "Written {} rows to file {}".format(len(table.rows), path), file=sys.stderr
        )
