from tabler.tabletype import TableType

from openpyxl import Workbook, load_workbook


class XLSX(TableType):

    extensions = ['.xlsx']

    def __init__(self, extension='.xlsx'):
        super().__init__(extension)

    def open(self, path):
        wb = load_workbook(filename=str(path))
        ws = wb.active
        data = []
        for row in ws:
            data.append([cell.value for cell in row])
        return data[0], data[1:]

    def write(self, table, path):
        wb = Workbook()
        ws = wb.active
        ws.append(table.header)
        for row in table:
            ws.append(row.row)
        wb.save(path)
        print('Writen ' + str(len(table.rows)) + ' lines to file ' + str(path))
