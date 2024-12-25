"""Project prompt generator script.

This script generates AI prompts by analyzing project files, respecting .gitignore rules
and custom directory exclusions.
"""

import argparse
import os
from dataclasses import dataclass
from typing import Dict, List

import pathspec


@dataclass
class GitignoreRule:
    """A class representing .gitignore rules."""

    patterns: pathspec.PathSpec
    base_dir: str

    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored by this rule set."""
        relative_path = os.path.relpath(path, self.base_dir)
        return self.patterns.match_file(relative_path)


class GitignoreManager:
    """Manager for handling .gitignore rules."""

    def __init__(self, base_dir: str):
        """Initialize the .gitignore manager.

        Args:
            base_dir: Base directory for searching .gitignore files.
        """
        self.base_dir = base_dir
        self.rules_cache = {}  # パスごとの.gitignoreルールをキャッシュ
        self._load_all_gitignores()

    def _parse_gitignore(self, gitignore_path: str) -> pathspec.PathSpec:
        """Parse a .gitignore file.

        Args:
            gitignore_path: Path to .gitignore file.

        Returns:
            Compiled gitignore patterns.
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

    def _load_all_gitignores(self):
        """Load all .gitignore files from the base directory and subdirectories."""
        for root, dirs, files in os.walk(self.base_dir):
            if ".gitignore" in files:
                gitignore_path = os.path.join(root, ".gitignore")
                patterns = self._parse_gitignore(gitignore_path)
                self.rules_cache[root] = GitignoreRule(patterns, root)

    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored by any .gitignore rule.

        Args:
            path: Path to check.

        Returns:
            True if the path should be ignored.
        """
        current_dir = os.path.dirname(path)
        while current_dir >= self.base_dir:
            if current_dir in self.rules_cache:
                if self.rules_cache[current_dir].is_ignored(path):
                    return True
            current_dir = os.path.dirname(current_dir)
        return False


class PromptGenerator:
    """Generator for creating AI prompts from project files."""

    def __init__(
        self, base_dir: str, file_patterns: List[str], exclude_dirs: List[str] = None
    ):
        """Initialize the prompt generator.

        Args:
            base_dir: Base directory to search.
            file_patterns: List of file patterns to include.
            exclude_dirs: List of directories to exclude.
        """
        self.base_dir = os.path.abspath(base_dir)
        self.file_patterns = file_patterns
        self.exclude_dirs = exclude_dirs or []
        self.gitignore_manager = GitignoreManager(self.base_dir)

    def should_skip_path(self, path: str) -> bool:
        """Determine if a path should be skipped.

        Args:
            path: Path to check.

        Returns:
            True if the path should be skipped.
        """
        if self.gitignore_manager.is_ignored(path):
            return True

        rel_path = os.path.relpath(path, self.base_dir)
        return any(
            rel_path == excluded
            or rel_path.startswith(f"{excluded}/")
            or rel_path.startswith(f"{excluded}\\")
            for excluded in self.exclude_dirs
        )

    def should_include_file(self, filename: str) -> bool:
        """Determine if a file should be included.

        Args:
            filename: Filename to check.

        Returns:
            True if the file should be included.
        """
        if filename in self.file_patterns:
            return True

        return any(filename.endswith(pattern) for pattern in self.file_patterns)

    def collect_files(self) -> Dict[str, str]:
        """Collect files matching the specified patterns.

        Returns:
            Dictionary mapping file paths to their contents.
        """
        collected_files = {}

        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [
                d for d in dirs if not self.should_skip_path(os.path.join(root, d))
            ]

            for file in files:
                file_path = os.path.join(root, file)

                if self.should_skip_path(file_path):
                    continue

                if self.should_include_file(file):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            collected_files[file_path] = content
                    except Exception as e:
                        print(f"Error reading file {file_path}: {str(e)}")

        return collected_files

    def generate_prompt(self, files_content: Dict[str, str]) -> str:
        """Generate an AI prompt from the collected files.

        Args:
            files_content: Dictionary mapping file paths to their contents.

        Returns:
            Generated prompt text.
        """
        if not files_content:
            return "対象となるファイルが見つかりませんでした。"

        prompt = "以下のプロジェクトファイルを確認してください：\n\n"

        sorted_files = sorted(files_content.items(), key=lambda x: x[0])

        for file_path, content in sorted_files:
            relative_path = os.path.relpath(file_path, self.base_dir)
            prompt += f"=== {relative_path} ===\n"
            prompt += content
            prompt += "\n\n"

        return prompt


def main():
    """Execute the main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate AI prompt from project files"
    )
    parser.add_argument("--dir", type=str, default=".", help="Base directory to search")
    parser.add_argument(
        "--patterns",
        type=str,
        nargs="+",
        default=[
            # 拡張子パターン
            ".py",
            ".js",
            ".ts",
            ".json",
            ".yml",
            ".yaml",
            ".html",
            ".conf",
            ".toml",
            ".md",
            ".css",
            ".scss",
            # 完全なファイル名パターン
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            ".env",
            ".gitignore",
            "Makefile",
            "requirements.txt",
            "package.json",
            "tsconfig.json",
            ".dockerignore",
        ],
        help="File patterns to include (extensions or complete filenames)",
    )
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument(
        "--exclude-dirs", type=str, nargs="+", help="Additional directories to exclude"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    generator = PromptGenerator(
        base_dir=args.dir, file_patterns=args.patterns, exclude_dirs=args.exclude_dirs
    )

    files_content = generator.collect_files()

    if args.verbose:
        print(f"Found {len(files_content)} files to process")

    prompt = generator.generate_prompt(files_content)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Prompt has been written to {args.output}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
