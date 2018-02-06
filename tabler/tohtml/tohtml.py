import os

from jinja2 import Template


class ToHTML:

    default_template = os.path.join(
        os.path.dirname(__file__), 'table_template.html')

    def __init__(self, table, use_header=True, template=None, escape=True):
        self.table = table
        self.escape = escape
        self.use_header = use_header
        self.template = self.get_template(template)
        self.context = self.get_context(table, self.use_header)

    def __str__(self):
        return self.render()

    @staticmethod
    def get_context(table, use_header):
        return {
            'use_header': use_header, 'header': table.header,
            'data': [r.row for r in table]}

    def get_template(self, template):
        if template is None:
            with open(self.default_template, 'r') as template_file:
                return Template(template_file.read())
        else:
            if isinstance(template, Template):
                return template
            else:
                return Template(template)

    def render(self):
        return self.template.render(self.context, autoescape=self.escape)
