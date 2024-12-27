"""Custom exceptions for the promptgen package."""


class PromptgenError(Exception):
    """Base exception for all promptgen errors."""


class FileAccessError(PromptgenError):
    """Raised when there is an error accessing a file."""


class GitignoreError(PromptgenError):
    """Raised when there is an error processing .gitignore files."""


class PatternError(PromptgenError):
    """Raised when there is an error with file patterns."""
