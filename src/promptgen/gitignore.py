"""Gitignore handling module."""

import os
from dataclasses import dataclass
from typing import Dict

import pathspec


@dataclass
class GitignoreRule:
    """Gitignore rule handler.

    Attributes:
        patterns: Compiled gitignore patterns
        base_dir: Base directory for this rule set
    """

    patterns: pathspec.PathSpec
    base_dir: str

    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored by this rule set.

        Args:
            path: Path to check

        Returns:
            bool: True if the path should be ignored
        """
        relative_path = os.path.relpath(path, self.base_dir)
        return self.patterns.match_file(relative_path)


class GitignoreManager:
    """Manager for handling multiple .gitignore rules."""

    def __init__(self, base_dir: str):
        """Initialize GitignoreManager.

        Args:
            base_dir: Base directory to start searching for .gitignore files
        """
        self.base_dir = base_dir
        self.rules_cache: Dict[str, GitignoreRule] = {}
        self._load_all_gitignores()

    def _parse_gitignore(self, gitignore_path: str) -> pathspec.PathSpec:
        """Parse a .gitignore file.

        Args:
            gitignore_path: Path to .gitignore file

        Returns:
            PathSpec: Compiled gitignore patterns
        """
        patterns = []
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception as e:
            print(f"Warning: Error reading {gitignore_path}: {str(e)}")

        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)

    def _load_all_gitignores(self) -> None:
        """Load all .gitignore files from base directory and subdirectories."""
        for root, dirs, files in os.walk(self.base_dir):
            if ".gitignore" in files:
                gitignore_path = os.path.join(root, ".gitignore")
                patterns = self._parse_gitignore(gitignore_path)
                self.rules_cache[root] = GitignoreRule(patterns, root)

    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored by any .gitignore rule.

        Args:
            path: Path to check

        Returns:
            bool: True if the path should be ignored
        """
        current_dir = os.path.dirname(path)
        while current_dir >= self.base_dir:
            if current_dir in self.rules_cache:
                if self.rules_cache[current_dir].is_ignored(path):
                    return True
            current_dir = os.path.dirname(current_dir)
        return False
