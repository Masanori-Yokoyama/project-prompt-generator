"""Test cases for Python API usage."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from promptgen import PromptGenerator


def test_api_basic_usage():
    """Test basic API usage."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_js = base_dir / "test.js"
        test_txt = base_dir / "test.txt"

        test_py.write_text("print('test')")
        test_js.write_text("console.log('test')")
        test_txt.write_text("test")

        # Use API
        generator = PromptGenerator(
            base_dir=str(base_dir),
            file_patterns=[".py", ".js"],
        )

        files = generator.collect_files()
        assert len(files) == 2
        assert str(test_py) in files
        assert str(test_js) in files
        assert str(test_txt) not in files

        prompt = generator.generate_prompt(files)
        assert "test.py" in prompt
        assert "test.js" in prompt
        assert "print('test')" in prompt
        assert "console.log('test')" in prompt


def test_api_with_gitignore():
    """Test API with .gitignore integration."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)

        # Create .gitignore
        gitignore = base_dir / ".gitignore"
        gitignore.write_text("*.txt\n")

        # Create test files
        test_py = base_dir / "test.py"
        test_txt = base_dir / "test.txt"

        test_py.write_text("print('test')")
        test_txt.write_text("ignored")

        # Use API
        generator = PromptGenerator(
            base_dir=str(base_dir),
            file_patterns=[".py", ".txt"],
        )

        files = generator.collect_files()
        assert len(files) == 1
        assert str(test_py) in files
        assert str(test_txt) not in files


def test_api_with_exclude_dirs():
    """Test API with directory exclusion."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        exclude_dir = base_dir / "exclude"
        exclude_dir.mkdir()

        # Create test files
        test_py = base_dir / "test.py"
        exclude_py = exclude_dir / "exclude.py"

        test_py.write_text("print('test')")
        exclude_py.write_text("print('exclude')")

        # Use API
        generator = PromptGenerator(
            base_dir=str(base_dir),
            file_patterns=[".py"],
            exclude_dirs=["exclude"],
        )

        files = generator.collect_files()
        assert len(files) == 1
        assert str(test_py) in files
        assert str(exclude_py) not in files


def test_api_error_handling():
    """Test API error handling."""
    # Test with non-existent directory
    with pytest.raises(NotADirectoryError):
        PromptGenerator(
            base_dir="/nonexistent/directory",
            file_patterns=[".py"],
        )

    # Test with empty patterns
    with pytest.raises(ValueError):
        PromptGenerator(
            base_dir=".",
            file_patterns=[],
        )
