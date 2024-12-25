"""Gitignore handling module."""

from dataclasses import dataclass
from pathlib import Path
from typing import List

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
        relative_path = Path(path).relative_to(self.base_dir).as_posix()
        return self.patterns.match_file(relative_path)


class GitignoreManager:
    """Manager for handling multiple .gitignore rules."""

    def __init__(self, base_dir: str):
        """Initialize GitignoreManager.

        Args:
            base_dir: Base directory to start searching for .gitignore files
        """
        self.base_dir = Path(base_dir).resolve()
        self.rules_cache: dict[str, GitignoreRule] = {}
        self._load_all_gitignores()

    def _parse_gitignore(self, gitignore_path: str) -> pathspec.PathSpec:
        """Parse a .gitignore file.

        Args:
            gitignore_path: Path to .gitignore file

        Returns:
            PathSpec: Compiled gitignore patterns
        """
        patterns: List[str] = []
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
        for path in Path(self.base_dir).rglob(".gitignore"):
            dir_path = str(path.parent)
            patterns = self._parse_gitignore(str(path))
            self.rules_cache[dir_path] = GitignoreRule(patterns, dir_path)

    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored by any .gitignore rule.

        Args:
            path: Path to check

        Returns:
            bool: True if the path should be ignored
        """
        path = Path(path).resolve()
        current_dir = path.parent

        # Check each parent directory for .gitignore rules
        while current_dir.as_posix() >= self.base_dir.as_posix():
            if str(current_dir) in self.rules_cache:
                if self.rules_cache[str(current_dir)].is_ignored(str(path)):
                    return True
            current_dir = current_dir.parent

        return False
