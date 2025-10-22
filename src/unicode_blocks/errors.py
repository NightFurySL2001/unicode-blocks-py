class UnicodeBlockError(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidUnicodeBlockNameError(UnicodeBlockError):
    """Exception raised for invalid Unicode block names."""

    pass
