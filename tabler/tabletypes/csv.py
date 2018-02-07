import csv

import requests
from tabler.tabletype import TableType


class CSV(TableType):

    extensions = ['.csv', '.txt']

    def __init__(self, encoding='utf-8', delimiter=',', extension='.csv'):
        self.encoding = encoding
        self.delimiter = delimiter
        super().__init__(extension)

    def open(self, path):
        open_file = open(path, 'rU', encoding=self.encoding)
        csv_file = csv.reader(open_file, delimiter=self.delimiter)
        rows = [row for row in csv_file]
        return rows[0], rows[1:]

    def write(self, table, path):
        csv_file = open(path, 'w', newline='', encoding=self.encoding)
        writer = csv.writer(csv_file, delimiter=self.delimiter)
        if table.header:
            writer.writerow(table.header)
        for row in table:
            writer.writerow(row.row)
        csv_file.close()
        print('Writen ' + str(len(table.rows)) + ' lines to file ' + str(path))


class CSVURL(CSV):

    def open(self, path):
        request = requests.get(path)
        text = []
        for line in request.iter_lines():
            if len(line) > 0:
                text.append(line.decode(self.encoding))
        csv_file = csv.reader(text)
        rows = [row for row in csv_file]
        return rows[0], rows[1:]
