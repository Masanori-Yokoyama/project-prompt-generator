"""Project Prompt Generator.

A tool to generate AI prompts from project files.

Example:
    Basic usage:
        >>> from promptgen import PromptGenerator
        >>> generator = PromptGenerator(
        ...     base_dir="./my_project",
        ...     file_patterns=[".py", ".js"],
        ...     exclude_dirs=["node_modules"]
        ... )
        >>> files = generator.collect_files()
        >>> prompt = generator.generate_prompt(files)
        >>> print(prompt)

    Using with custom patterns:
        >>> generator = PromptGenerator(
        ...     base_dir=".",
        ...     file_patterns=["Dockerfile", "docker-compose.yml", ".env"]
        ... )
        >>> files = generator.collect_files()
        >>> prompt = generator.generate_prompt(files)
"""

__version__ = "0.1.0"

from .generator import PromptGenerator
from .gitignore import GitignoreManager, GitignoreRule

__all__ = ["PromptGenerator", "GitignoreManager", "GitignoreRule"]
