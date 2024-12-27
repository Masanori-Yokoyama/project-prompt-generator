"""Test cases for gitignore module."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pathspec
import pytest

from promptgen.exceptions import GitignoreError
from promptgen.gitignore import GitignoreManager, GitignoreRule


def test_gitignore_rule():
    """Test GitignoreRule basic functionality."""
    patterns = pathspec.PathSpec.from_lines(
        "gitwildmatch", ["*.pyc", "__pycache__/", "*.log"]
    )
    rule = GitignoreRule(patterns=patterns, base_dir="/test")

    assert rule.is_ignored("/test/file.pyc")
    assert not rule.is_ignored("/test/file.py")


def test_gitignore_rule_error():
    """Test GitignoreRule error handling."""
    patterns = pathspec.PathSpec.from_lines("gitwildmatch", ["*.pyc"])
    rule = GitignoreRule(patterns=patterns, base_dir="/test")

    # 無効なパスでテスト（相対パスの計算が不可能なケース）
    invalid_path = os.path.join("/test", "..", "..", "invalid")  # /test より上の階層に移動
    with pytest.raises(GitignoreError) as excinfo:
        rule.is_ignored(invalid_path)
    assert "Error processing path" in str(excinfo.value)


def test_gitignore_manager():
    """Test GitignoreManager functionality."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        sub_dir = base_dir / "subdir"
        sub_dir.mkdir()

        # Create .gitignore files
        with open(base_dir / ".gitignore", "w") as f:
            f.write("*.pyc\n")
            f.write("__pycache__/\n")

        with open(sub_dir / ".gitignore", "w") as f:
            f.write("*.log\n")

        # Initialize manager
        manager = GitignoreManager(str(base_dir))

        # Test file matching
        assert manager.is_ignored(str(base_dir / "test.pyc"))
        assert manager.is_ignored(str(sub_dir / "test.log"))
        assert not manager.is_ignored(str(base_dir / "test.py"))


def test_gitignore_manager_with_nested_rules():
    """Test GitignoreManager with nested rules."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        level1_dir = base_dir / "level1"
        level2_dir = level1_dir / "level2"
        os.makedirs(level2_dir)

        # Create .gitignore files at different levels
        with open(base_dir / ".gitignore", "w") as f:
            f.write("*.pyc\n")

        with open(level1_dir / ".gitignore", "w") as f:
            f.write("*.log\n")

        with open(level2_dir / ".gitignore", "w") as f:
            f.write("*.tmp\n")

        manager = GitignoreManager(str(base_dir))

        # Test file matching at different levels
        assert manager.is_ignored(str(base_dir / "test.pyc"))
        assert manager.is_ignored(str(level1_dir / "test.log"))
        assert manager.is_ignored(str(level2_dir / "test.tmp"))
        assert not manager.is_ignored(str(base_dir / "test.txt"))


def test_gitignore_manager_file_error(caplog):
    """Test GitignoreManager file reading error handling."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)

        # 読み取り権限のない.gitignoreファイルを作成
        gitignore = base_dir / ".gitignore"
        gitignore.write_text("*.log")
        gitignore.chmod(0o000)  # 読み取り権限を削除

        # GitignoreManagerの初期化（警告ログを確認）
        manager = GitignoreManager(str(base_dir))
        assert "Error reading" in caplog.text

        # managerが初期化されていることを確認
        test_file = base_dir / "test.log"
        assert not manager.is_ignored(str(test_file))  # ファイルが読めないため無視されない

        # 後処理：ファイルの権限を戻す
        gitignore.chmod(0o644)


def test_gitignore_manager_invalid_base_dir():
    """Test GitignoreManager with invalid base directory."""
    with pytest.raises(GitignoreError) as excinfo:
        GitignoreManager("/nonexistent/directory")
    assert "Base directory not found" in str(excinfo.value)
