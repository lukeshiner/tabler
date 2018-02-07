r"""tabletypes package.

The tabletypes package provides the :class:`tabler.tabletypes.BaseTableType`
class which can be subclassed to provided open and write methods to
:class:`tabler.Table`.

They can be customised by providing paramaters to the __init__ method.

Also provides subclasses of :class:`table.tabletypes.BaseTableType` for
common file types.

- :class:`tabler.tabletypes.CSV` Open and write .csv files.
- :class:`tabler.tabletypes.CSVURL` Open .csv over HTTP.
- :class:`tabler.tabletypes.HTML`: Save table as .html file.
- :class:`tabler.tabletypes.ODS`: Open and save Open Document
    Spreadsheed (.ods) files.
- :class:`tabler.tabletypes.XLSX`: Open and save Microsoft Excel (.xlsx) files.

Basic Usage::

    from tabler import Table
    from tabler.tabletypes import CSV

    table = Table('path/to/open.csv', table_type=CSV())
    table.save('path/to/save.csv', table_type=CSV())

Usage with paramaters::

    from tabler import Table
    from tabler.tabletypes import CSV

    table = Table('path/to/open.csv', table_type=CSV(
        extension='.txt', delimiter='\t', encoding='latin'))
    table.save('path/to/save.csv', table_type=CSV(
        extension='.txt', delimiter='\t', encoding='latin'))

Alternate Usage::

    from tabler import Table
    from tabler.tabletypes import CSV

    csv = CSV(delimiter='\t', delimiter='\t', encoding='latin')
    table = Table('path/to/open.csv', table_type=csv)
    table.save('path/to/save.csv', table_type=csv)
"""
from . basetabletype import BaseTableType  # NOQA
from . csv import CSV, CSVURL  # NOQA
from . ods import ODS  # NOQA
from . html import HTML  # NOQA
from . xlsx import XLSX  # NOQA
