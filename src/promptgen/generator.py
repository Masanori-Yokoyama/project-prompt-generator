"""Prompt generator module."""


class PromptGenerator:
    """Main prompt generator class."""

    def __init__(self, base_dir: str, file_patterns: list, exclude_dirs: list = None):
        """Initialize the PromptGenerator.

        Args:
            base_dir: Base directory to search.
            file_patterns: List of file patterns to include.
            exclude_dirs: List of directories to exclude.
        """
        self.base_dir = base_dir
        self.file_patterns = file_patterns
        self.exclude_dirs = exclude_dirs or []
