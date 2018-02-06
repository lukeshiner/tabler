from . import exceptions


def all_subclasses(cls):
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in all_subclasses(s)]


class TableType:

    def __init__(self, extension):
        self.extension = extension

    @classmethod
    def get_by_extension(cls, extension):
        for table_type in all_subclasses(cls):
            if extension.lower() in table_type.extensions:
                return table_type()
        raise exceptions.ExtensionNotRecognised(extension)

    def open(self, path):
        raise NotImplementedError

    def write(self, table, path):
        raise NotImplementedError
