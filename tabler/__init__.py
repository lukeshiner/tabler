# -*- coding: utf-8 -*-

"""
Tabler package
~~~~~~~~~~~~~~

The tabler package provides the Table class for simple and intutive accessing,
manipulation and writing of tablulated data in .csv format.

    Basic Usage::

        >>> import Table
        >>> table = Table.Table()
        >>> table.open('Path/To/Input_File.csv')
        CsvFile Object containing 3 colomuns and 3 rows
        Column Headings: SKU, Item Title, Price
        >>> table[0]['Price']
        '29.99'
        >>> table[0]['Price'] = 15.50
        >>> table[0]['Price']
        '15.5'
        >>> table.write('Path/To/Output_File.csv')
        Writen 3 lines to file Path/To/Output_File.csv

Formats other than .csv are supported. See full documentation <LINK TO DOCS>

"""

__title__ = 'tabler'
__version__ = '1.0.02'
__author__ = 'Luke Shiner'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Luke Shiner'

from .tabler import Table
