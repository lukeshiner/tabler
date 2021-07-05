"""Exceptions for tabler package."""


class ExtensionNotRecognised(ValueError):
    """Error finding TableType subclass by file extension."""

    def __init__(self, extension: str) -> None:
        """
        Initialise ExtensionNotRecognised exception.

        :param str extension: File extension for which no TableType was found.
        """
        super().__init__("Extension '{}' not recognised.".format(extension))


class TableInitialisationError(TypeError):
    """Error initialising table due to incorrect arguments."""

    def __init__(self) -> None:
        """Initialise TableInitialisationError exception."""
        super().__init__(
            "Table cannot be initialised. "
            "Either filepath or header and data must be specified."
        )
