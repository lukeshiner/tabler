#!/usr/bin/python3

# TableRow by Luke Shiner (luke@lukeshiner.com)


class TableRow(object):
    """ Container for a row of data. Used by Table object. """

    def __init__(self, row, header):
        self.row = row
        self.header = header
        self.headers = {}

        for column in self.header:
            self.headers[column] = self.header.index(column)

    def __iter__(self):
        for item in self.row:
            yield item

    def __getitem__(self, index):
        if type(index) == int:
            return self.row[index]
        elif type(index) == str:
            return self.row[self.headers[index]]

    def __setitem__(self, key, item):
        if type(key) == int:
            self.row[key] = str(item)
        elif type(key) == str:
            self.row[self.headers[key]] = str(item)

    def __str__(self):
        new_string = ""
        for item in self.to_array():
            new_string = new_string + "'" + item + "', "
        return new_string[0:-2]

    def __len__(self):
        return len(self.row)

    def get_column(self, column):
        """ Returns the value held in the specified column.  """
        return self.row[self.headers[column]]

    def update_column(self, column, value):
        self.row[self.headers[column]] = str(value)

    def remove_column(self, column):
        """ Removes the specified column.  """
        if column in self.header:
            columnIndex = self.header.index(column)
            self.row.pop(columnIndex)
            self.header.pop(columnIndex)
        else:
            return False

    def to_array(self):
        """ Returns the data row as a list object.  """
        return self.row

    def copy(self):
        return TableRow(self.row, self.header)
