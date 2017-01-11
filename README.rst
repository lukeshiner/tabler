=============
Tabler Readme
=============
--------------------------------------
Simple interaction with tabulated data
--------------------------------------

.. contents:: Contents

What is tabler?
===============

The tabler package provides the Tabler class which is intended to make the creation and maniplulation of tabulated data intuitive.

It can:
    + Open .csv files from a relative path, absolute path or url
    + Update text in cells
    + Write out .csv files
    + Read and write .ods files (**Experimental**)

Tabler is not, however, a spreadsheet. It is designed for manipulating tables
of text. Users looking for complex mathematical operations may be better
served by numpy (http://www.numpy.org/)

Quick Start
===========

Creating a Table (Basic)
________________________

Import the Tabler class from the tabler package and instanciate it::

    from tabler import Tabler

    table = Tabler()

Tabler requires a column names. The column names are a list of strings located at ``Tabler().header``.
Many of tabler's functions will not work as intended without a header supplied, therefore when creating blank tables
it is highly reccomended that a header be specified at instanciation by creating the necessary list and passing it to
the ``header`` keyword argument of it's ``__init__()`` function::

    header = ['SKU', 'Item Title', 'Price']
    table = Tabler(header=header)

Alternativly ``table.header`` can be set directly after instanciation::

    table.header = ['SKU', 'Item Title', 'Price']


Opening a Table (Basic)
_______________________
Table will take a relative or absolute path or a URL it's first positional argument.

If the string begins with 'http://' or 'https://' it will use the ``requests`` module to attempt to open a ``.csv`` file at the indicated resource::

    Tabler('http://www.example.com/stock.csv')


If the string ends with '.csv' it will atempt to open the file at the specified location as a ``.csv`` file::

    Tabler('Desktop/stock.csv')

If the string ends with '.ods' it will atempt to open the file as an Open Doucument Format spreadsheet (``.ods``)::

    Tabler('Desktop/stock.ods')

Reading a Table (Basic)
_______________________

At its base, Tabler is a two dimensional ``list``. Therefore the simplest way to access a cell is by providing two indexes::

    first_cell = table[0][0]

Rows can be indexed by row number (zero based)
Tabler will always treat the first line of any supplied data as column headers.
This means that a column can be specified by index number or title::

    first_item_title = table[0]["Item Title"]

Editing a Table (Basic)
_______________________

A cell can be edited using the equals ``=`` operator::

    table[2]["Item Title"] = 'USB Hub'

Cell content can be ``string``, ``int`` or ``float``.

Loading Data into a Table (Basic)
_________________________________

Data can be loaded into an empty Tabler object by passing a ``list`` of rows in the form of ``lists`` of cell data using the ``Tabler().load_from_array(data, header)`` method. A ``list`` of column headers must be passed as the second argument::

    header = ["SKU", "Item Title", "Price"]

    data = [
        ["001", "USB Hub", 7.00],
        ["002", "Raspberry Pi 3", 29.99],
        ["003", Arduino Uno", 20.00]
    ]

    table = Tabler()
    table.load_from_array(data, header)

Writing a Table to a File (Basic)
_________________________________

To write a basic ``.csv`` file of the data in a Tabler object call the ``.write`` method and pass a filepath::

    table.write('Desktop/stock.csv')

An ods file can be written with the ``Tabler.write_ods`` method, note, however, that all cells will be written as strings::

    table.write_ods('Desktop/stock.ods')

General Use
=================

Creating a Table
________________

Opening a Table
_______________

Editing a Table
_______________

Writing a Table
_______________

Sorting a Table
_______________

Working with HTML Tables
________________________

Working with Open Document Spreadsheet (.ods) Tables
____________________________________________________


Appendix
========

Contact
_______

All comments and queries can be sent to Luke Shiner at luke@lukeshiner.com

License
_______

Distributed with MIT License.

Credits
_______

Created by Luke Shiner (luke@lukeshiner.com)
