"""Test cases for command line interface."""

from pathlib import Path
from tempfile import TemporaryDirectory

from promptgen.cli import main


def test_cli_basic_functionality():
    """Test basic CLI functionality."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")

        # Test with minimal arguments
        args = ["--dir", str(base_dir)]
        assert main(args) == 0


def test_cli_output_file():
    """Test CLI output to file."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")

        # Create output file
        output_file = base_dir / "output.txt"
        args = ["--dir", str(base_dir), "--output", str(output_file)]
        assert main(args) == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "test.py" in content
        assert "print('test')" in content


def test_cli_verbose_output(capsys):
    """Test CLI verbose output."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")

        # Test with verbose flag
        args = ["--dir", str(base_dir), "--verbose"]
        assert main(args) == 0

        # Check stderr output
        captured = capsys.readouterr()
        assert "Scanning directory:" in captured.err
        assert "File patterns:" in captured.err
        assert "Found 1 files to process" in captured.err


def test_cli_exclude_dirs():
    """Test CLI directory exclusion."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        base_dir = Path(temp_dir)
        exclude_dir = base_dir / "exclude"
        exclude_dir.mkdir()
        test_py = exclude_dir / "test.py"
        test_py.write_text("print('test')")

        # Test with exclude directory
        args = ["--dir", str(base_dir), "--exclude-dirs", "exclude"]
        assert main(args) == 0


def test_cli_error_handling(capsys):
    """Test CLI error handling."""
    # Test with non-existent directory
    args = ["--dir", "/nonexistent/directory"]
    assert main(args) == 1
    captured = capsys.readouterr()
    assert "Error: Directory not found:" in captured.err

    # Test with invalid output file path
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")
        args = ["--dir", str(base_dir), "--output", "/nonexistent/output.txt"]
        assert main(args) == 1
        captured = capsys.readouterr()
        assert "Error writing to output file:" in captured.err


def test_cli_exclude_dirs_verbose(capsys):
    """Test CLI with exclude directories and verbose output."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        exclude_dir = base_dir / "exclude"
        exclude_dir.mkdir()

        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")

        args = ["--dir", str(base_dir), "--exclude-dirs", "exclude", "--verbose"]
        assert main(args) == 0

        captured = capsys.readouterr()
        assert "Excluding directories: ['exclude']" in captured.err


def test_cli_output_verbose(capsys):
    """Test CLI output with verbose option."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")
        output_file = base_dir / "output.txt"

        args = ["--dir", str(base_dir), "--output", str(output_file), "--verbose"]
        assert main(args) == 0

        captured = capsys.readouterr()
        assert f"Output written to: {output_file}" in captured.err


def test_cli_general_error(capsys):
    """Test CLI general error handling."""
    # 一般的な例外を発生させる
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        output_file = base_dir / "nonexistent" / "output.txt"  # 存在しないディレクトリ内のファイル

        args = ["--dir", str(base_dir), "--output", str(output_file)]
        assert main(args) == 1

        captured = capsys.readouterr()
        assert "Error writing to output file:" in captured.err


def test_cli_unexpected_error(capsys, monkeypatch):
    """Test CLI unexpected error handling."""

    def mock_parse_args(args):
        raise ValueError("Mock error")

    # parse_args関数をモック化して確実に例外を発生させる
    monkeypatch.setattr("promptgen.cli.parse_args", mock_parse_args)

    args = ["--dir", "."]
    assert main(args) == 1

    captured = capsys.readouterr()
    assert "Error: Mock error" in captured.err
