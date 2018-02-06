from tabler.tabletype import TableType
from tabler.tohtml import ToHTML


class HTML(TableType):

    extensions = ['.html']

    def __init__(self, use_header=True, encoding='utf8', extension='.html'):
        self.encoding = encoding
        self.use_header = use_header
        super().__init__(extension)

    def write(self, table, path):
        html = ToHTML(table, self.use_header).render()
        html_file = open(path, 'w', encoding=self.encoding)
        html_file.write(html)
        html_file.close()
        print('Writen ' + str(len(table.rows)) + ' lines to file ' + str(path))
