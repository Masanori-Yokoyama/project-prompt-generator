"""Test cases for generator module."""

from pathlib import Path
from tempfile import TemporaryDirectory

from promptgen.generator import PromptGenerator


def test_prompt_generator():
    """Test PromptGenerator functionality."""
    with TemporaryDirectory() as temp_dir:
        # Create test directory structure
        base_dir = Path(temp_dir)
        sub_dir = base_dir / "subdir"
        exclude_dir = base_dir / "exclude"
        sub_dir.mkdir()
        exclude_dir.mkdir()

        # Create test files
        test_py = base_dir / "test.py"
        test_js = sub_dir / "test.js"
        test_txt = base_dir / "test.txt"
        test_exclude = exclude_dir / "test.py"

        test_py.write_text("print('test')")
        test_js.write_text("console.log('test')")
        test_txt.write_text("test")
        test_exclude.write_text("print('exclude')")

        # Create .gitignore
        gitignore = base_dir / ".gitignore"
        gitignore.write_text("*.txt\n")

        # Initialize generator
        generator = PromptGenerator(
            base_dir=str(base_dir),
            file_patterns=[".py", ".js"],
            exclude_dirs=["exclude"],
        )

        # Test file collection
        files = generator.collect_files()
        assert len(files) == 2
        assert str(test_py) in files
        assert str(test_js) in files
        assert str(test_txt) not in files
        assert str(test_exclude) not in files

        # Test prompt generation
        prompt = generator.generate_prompt(files)
        assert "test.py" in prompt
        assert "subdir/test.js" in prompt
        assert "print('test')" in prompt
        assert "console.log('test')" in prompt
