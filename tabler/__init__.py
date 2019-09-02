"""
Tabler package.

The tabler package provides the :class:`tabler.Table` class for simple and
intutive accessing, manipulation and writing of tablulated data.

    Basic Usage::

        >>> from tabler import Table
        >>> table = Table('somefile.csv')
        >>> table.open('Path/To/Input_File.csv')
        >>> table[0]['Price']
        '29.99'
        >>> table[0]['Price'] = 15.50
        >>> table[0]['Price']
        '15.5'
        >>> table.write('Path/To/Output_File')
        Writen 3 lines to file Path/To/Output_File.csv

"""

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from .table import Table
from .tabletypes import CSV, CSVURL, HTML, ODS, XLSX

__all__ = [
    "Table",
    "CSV",
    "CSVURL",
    "HTML",
    "ODS",
    "XLSX",
    "__author_email__",
    "__author__",
    "__copyright__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
]
