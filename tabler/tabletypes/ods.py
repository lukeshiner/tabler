from collections import OrderedDict

from tabler.tabletype import TableType

import ezodf
from pyexcel_ods3 import save_data


class ODS(TableType):

    extensions = ['.ods']

    def __init__(self, sheet=0, extension='.ods'):
        self.sheet = sheet
        super().__init__(extension)

    def open(self, path):
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
        data = OrderedDict()
        sheet = [table.header]
        sheet += table.rows
        data.update({"Sheet 1": sheet})
        save_data(str(path), data)
        print('Writen ' + str(len(table.rows)) + ' lines to file ' + str(path))
