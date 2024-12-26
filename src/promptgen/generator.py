"""File collection and prompt generation module."""

import os
from typing import Dict, List

from promptgen.gitignore import GitignoreManager


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

        Raises:
            NotADirectoryError: If base_dir does not exist or is not a directory.
            ValueError: If file_patterns is empty.
        """
        if not os.path.isdir(base_dir):
            raise NotADirectoryError(f"Directory not found: {base_dir}")
        if not file_patterns:
            raise ValueError("At least one file pattern must be specified")

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
        # .gitignoreルールのチェック
        if self.gitignore_manager.is_ignored(path):
            return True

        # 除外ディレクトリのチェック
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
        # 完全なファイル名のマッチング
        if filename in self.file_patterns:
            return True

        # 拡張子のマッチング
        return any(filename.endswith(pattern) for pattern in self.file_patterns)

    def collect_files(self) -> Dict[str, str]:
        """Collect files matching the specified patterns.

        Returns:
            Dictionary mapping file paths to their contents.
        """
        collected_files = {}

        for root, dirs, files in os.walk(self.base_dir):
            # 除外すべきディレクトリを削除
            dirs[:] = [
                d for d in dirs if not self.should_skip_path(os.path.join(root, d))
            ]

            for file in files:
                file_path = os.path.join(root, file)

                # パスをスキップすべきかチェック
                if self.should_skip_path(file_path):
                    continue

                # ファイル名または拡張子チェック
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

        # ファイルパスでソート
        sorted_files = sorted(files_content.items(), key=lambda x: x[0])

        for file_path, content in sorted_files:
            relative_path = os.path.relpath(file_path, self.base_dir)
            prompt += f"=== {relative_path} ===\n"
            prompt += content
            prompt += "\n\n"

        return prompt
