"""Exceptions for tabler package."""


class ExtensionNotRecognised(Exception):
    """Error finding TableType subclass by file extension."""

    def __init__(self, extension):
        """Initialise ExtensionNotRecognised exception.

        :param str extension: File extension for which no TableType was found.
        """
        super().__init__("Extension '{}' not recognised.".format(extension))
