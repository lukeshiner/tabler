"""This module a Table Type for writing tables as HTML."""

from tabler.tohtml import ToHTML

from .basetabletype import BaseTableType


class HTML(BaseTableType):
    """Table Type for comma separated value (.csv) files.

    :param bool use_header: If True file will include column headers.
        Default(True)
    :param str encoding: Encoding of file. Default: utf8.
    :param str extension: Extension of file to save. Default .html.
    :param verbose: If True print status messages. If None use
        :class:`tabler.tabletype.BaseTableType`.verbose.
    :type verbose: bool or None.
    """

    extensions = ['.html']

    def __init__(
            self, use_header=True, encoding='utf8', extension='.html',
            verbose=True):
        """Consturct :class:`tabler.tabletypes.HTML`.

        :param bool use_header: If True file will include column headers.
            Default(True)
        :param str encoding: Encoding of file. Default: utf8.
        :param str extension: Extension of file to save. Default .html.
        :param verbose: If True print status messages. If None use
            :class:`tabler.tabletype.BaseTableType`.verbose.
        :type verbose: bool or None.
        """
        self.encoding = encoding
        self.use_header = use_header
        super().__init__(extension, verbose=verbose)

    def write(self, table, path):
        """Save data from :class:`tabler.Table` to file.

        :param table: Table to save.
        :type table: :class:`tabler.Table`
        :param path: Path to file to be opened.
        :type path: str, pathlib.Path or compatible.
        """
        html = ToHTML(table, self.use_header).render()
        html_file = open(path, 'w', encoding=self.encoding)
        html_file.write(html)
        html_file.close()
        print('Written {} rows to file {}'.format(len(table.rows), path))
