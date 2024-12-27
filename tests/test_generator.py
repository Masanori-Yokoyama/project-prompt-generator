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


def test_prompt_generator_file_collection():
    """Test PromptGenerator file collection functionality."""
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


def test_prompt_generator_prompt_generation():
    """Test PromptGenerator prompt generation functionality."""
    with TemporaryDirectory() as temp_dir:
        # Create test directory structure
        base_dir = Path(temp_dir)
        sub_dir = base_dir / "src"
        sub_dir.mkdir()

        # Create test files with different content types
        files = {
            "main.py": "def main():\n    print('Hello')\n",
            "src/utils.py": "def helper():\n    return True\n",
            "config.json": '{"key": "value"}\n',
        }

        # Write test files
        for path, content in files.items():
            file_path = base_dir / path
            file_path.parent.mkdir(exist_ok=True)
            file_path.write_text(content)

        # Initialize generator
        generator = PromptGenerator(
            base_dir=str(base_dir), file_patterns=[".py", ".json"]
        )

        # Collect files and generate prompt
        collected_files = generator.collect_files()
        prompt = generator.generate_prompt(collected_files)

        # Verify prompt structure and content
        assert "=== main.py ===" in prompt
        assert "=== src/utils.py ===" in prompt
        assert "=== config.json ===" in prompt
        assert "def main():" in prompt
        assert "def helper():" in prompt
        assert '"key": "value"' in prompt

        # Verify file order
        main_pos = prompt.find("=== main.py ===")
        config_pos = prompt.find("=== config.json ===")
        utils_pos = prompt.find("=== src/utils.py ===")
        assert config_pos < main_pos < utils_pos  # Alphabetical order


def test_prompt_generator_empty_result():
    """Test PromptGenerator behavior with no matching files."""
    with TemporaryDirectory() as temp_dir:
        # Create test directory with no matching files
        base_dir = Path(temp_dir)
        test_txt = base_dir / "test.txt"
        test_txt.write_text("test")

        # Initialize generator with patterns that won't match
        generator = PromptGenerator(
            base_dir=str(base_dir), file_patterns=[".py", ".js"]
        )

        # Test empty file collection
        files = generator.collect_files()
        assert len(files) == 0

        # Test prompt generation with empty files
        prompt = generator.generate_prompt(files)
        assert prompt == "対象となるファイルが見つかりませんでした。"


def test_prompt_generator_exact_filename_match():
    """Test PromptGenerator with exact filename matching."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)

        # 完全なファイル名でマッチするファイルを作成
        dockerfile = base_dir / "Dockerfile"
        dockerfile.write_text("FROM python:3.8")

        # 完全なファイル名でマッチするパターンを指定
        generator = PromptGenerator(
            base_dir=str(base_dir), file_patterns=["Dockerfile"]  # 完全なファイル名を指定
        )

        files = generator.collect_files()
        assert len(files) == 1
        assert str(dockerfile) in files


def test_prompt_generator_file_read_error(capsys):
    """Test PromptGenerator file reading error handling."""
    with TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)

        # 読み取り権限のないファイルを作成
        test_py = base_dir / "test.py"
        test_py.write_text("print('test')")
        test_py.chmod(0o000)  # 読み取り権限を削除

        generator = PromptGenerator(base_dir=str(base_dir), file_patterns=[".py"])

        files = generator.collect_files()
        assert len(files) == 0

        # エラーメッセージを確認
        captured = capsys.readouterr()
        assert "Error reading file" in captured.out
        assert str(test_py) in captured.out

        # 後処理：ファイルの権限を戻す
        test_py.chmod(0o644)
