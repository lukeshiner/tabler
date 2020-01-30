"""Convert tabler tables to HTML."""

import os

from jinja2 import Template


class ToHTML:
    """Convert tabler tables to HTML."""

    default_template = os.path.join(os.path.dirname(__file__), "table_template.html")

    def __init__(self, table, use_header=True, template=None, escape=True):
        """Convert tabler tables to HTML."""
        self.table = table
        self.escape = escape
        self.use_header = use_header
        self.template = self.get_template()
        self.context = self.get_context(table, self.use_header)

    @staticmethod
    def get_context(table, use_header):
        """Return template context."""
        return {
            "use_header": use_header,
            "header": table.header,
            "data": [list(row) for row in table],
        }

    def get_template(self):
        """Return HTML template."""
        with open(self.default_template, "r") as template_file:
            return Template(template_file.read())

    def render(self):
        """Return rendered HTML."""
        return self.template.render(self.context, autoescape=self.escape)
