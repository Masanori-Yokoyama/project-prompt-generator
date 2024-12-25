"""Test cases for gitignore module."""

from promptgen.gitignore import GitignoreManager, GitignoreRule


def test_gitignore_rule():
    """Test GitignoreRule basic functionality."""
    rule = GitignoreRule(patterns=None, base_dir=".")
    assert isinstance(rule, GitignoreRule)


def test_gitignore_manager():
    """Test GitignoreManager basic functionality."""
    manager = GitignoreManager(base_dir=".")
    assert isinstance(manager, GitignoreManager)
