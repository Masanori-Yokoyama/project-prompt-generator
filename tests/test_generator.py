"""Test cases for generator module."""

from promptgen.generator import PromptGenerator


def test_prompt_generator():
    """Test PromptGenerator basic functionality."""
    generator = PromptGenerator(base_dir=".", file_patterns=[".py"], exclude_dirs=None)
    assert isinstance(generator, PromptGenerator)
