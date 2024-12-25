"""Gitignore handling module."""

from dataclasses import dataclass
from typing import Any


@dataclass
class GitignoreRule:
    """Gitignore rule handler."""

    patterns: Any
    base_dir: str


class GitignoreManager:
    """Gitignore rules manager."""

    def __init__(self, base_dir: str):
        """Initialize the GitignoreManager.

        Args:
            base_dir: Base directory to search for .gitignore files.
        """
        self.base_dir = base_dir
