"""Custom exceptions for mistune-json."""


class MistuneJSONError(Exception):
    """Base exception for mistune-json."""

    pass


class MistuneJSONValidationError(MistuneJSONError):
    """Raised when input validation fails."""

    pass

