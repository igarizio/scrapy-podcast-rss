"""This module defines custom exceptions
"""


class InvalidItemException(Exception):
    """Exception for when the pipeline tries to process an non-supported item."""
    pass
