"""Test cases for custom exceptions."""


from promptgen.exceptions import (
    FileAccessError,
    GitignoreError,
    PatternError,
    PromptgenError,
)


def test_exception_hierarchy():
    """Test exception class hierarchy."""
    assert issubclass(FileAccessError, PromptgenError)
    assert issubclass(GitignoreError, PromptgenError)
    assert issubclass(PatternError, PromptgenError)


def test_exception_messages():
    """Test exception messages."""
    file_error = FileAccessError("Cannot read file")
    assert str(file_error) == "Cannot read file"

    gitignore_error = GitignoreError("Invalid .gitignore")
    assert str(gitignore_error) == "Invalid .gitignore"

    pattern_error = PatternError("Invalid pattern")
    assert str(pattern_error) == "Invalid pattern"
