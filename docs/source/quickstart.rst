Quick Start
===========

Creating a Table
________________

Import the Tabler class from the tabler package and instantiate it with a header
and data::

    from tabler import Table

    table = Tabler(
        header=['SKU', 'Item Title', 'Price'],
        data=[[009, 'Item 1', 5.00], [010, 'Item 2', 9.99]])

Or pass the path to a file to open::

    from tabler import Table

    Table('path/to/some/file.csv')

This will recognise file types with the following extensions:
    + .csv (UTF-8 encoded and comma delimited).
    + .txt (UTF-8 encoded and comma delimited).
    + .xlsx
    + .ods

To explicitly open a file of a specific type you must provide a **Table Type**
object.::

    from tabler import Table
    from tabler.tabletypes import CSV

    Table('path/to/some/file.csv', table_type=CSV(delimiter='\t'))

**Table Types** subclass ``BaseTableType``. They tell tabler how to open and
write files.


Reading a Table
_______________

At its base, Tabler is a two dimensional ``list``. Therefore the simplest way
to access a cell is by providing two indexes::

    first_cell = table[0][0]

You can index a row by row number (zero based)
Tabler will always treat the first line of any supplied data as column headers.
This means that you can specify a column by index number or title::

    first_item_title = table[0]["Item Title"]

Editing a Table
_______________

Edit cells using the equals ``=`` operator::

    table[2]["Item Title"] = 'USB Hub'

Cell content can be ``string``, ``int`` or ``float``.

Loading Data into a Table
_________________________

You can load data into an empty Tabler object by passing a ``list`` of rows in
the form of ``lists`` of cell data using the
``Tabler().load_from_array(data, header)`` method. Pass A ``list`` of column
headers as the second argument::

    header = ["SKU", "Item Title", "Price"]

    data = [
        ["001", "USB Hub", 7.00],
        ["002", "Raspberry Pi 3", 29.99],
        ["003", Arduino Uno", 20.00]
    ]

    table = Tabler()
    table.load_from_array(data, header)

Writing a Table to a File
_________________________

Writing a file is similar to reading a file. Use ``Table Types`` in the same way
to manage writing files::

    table.write('path/to/save.csv', table_type=CSV(delimiter='\t')

Tabler will the ``table type`` automatically for recognised file extensions if
not explicitly set.
