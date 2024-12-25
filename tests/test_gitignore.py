"""Test cases for gitignore module."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pathspec

from promptgen.gitignore import GitignoreManager, GitignoreRule


def test_gitignore_rule():
    """Test GitignoreRule basic functionality."""
    # Create a PathSpec with some patterns
    patterns = pathspec.PathSpec.from_lines(
        "gitwildmatch", ["*.pyc", "__pycache__/", "*.log"]
    )
    rule = GitignoreRule(patterns=patterns, base_dir="/test")

    # Test matching
    assert rule.is_ignored("/test/file.pyc")
    assert rule.is_ignored("/test/__pycache__/module.pyc")
    assert rule.is_ignored("/test/logs/test.log")
    assert not rule.is_ignored("/test/file.py")
    assert not rule.is_ignored("/test/cache/file.txt")


def test_gitignore_manager():
    """Test GitignoreManager functionality."""
    with TemporaryDirectory() as temp_dir:
        # Create test directory structure
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
        assert manager.is_ignored(str(base_dir / "__pycache__"))
        assert manager.is_ignored(str(sub_dir / "test.log"))
        assert not manager.is_ignored(str(base_dir / "test.py"))
        assert not manager.is_ignored(str(base_dir / "test.txt"))


def test_gitignore_manager_with_nested_rules():
    """Test GitignoreManager with nested rules."""
    with TemporaryDirectory() as temp_dir:
        # Create nested directory structure
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
        assert manager.is_ignored(str(level1_dir / "test.pyc"))
        assert manager.is_ignored(str(level2_dir / "test.pyc"))
        assert manager.is_ignored(str(level1_dir / "test.log"))
        assert manager.is_ignored(str(level2_dir / "test.log"))
        assert manager.is_ignored(str(level2_dir / "test.tmp"))
        assert not manager.is_ignored(str(base_dir / "test.log"))
        assert not manager.is_ignored(str(base_dir / "test.tmp"))
