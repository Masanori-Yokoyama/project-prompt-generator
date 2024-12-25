"""Project Prompt Generator.

A tool to generate AI prompts from project files.
"""

__version__ = "0.1.0"

from .generator import PromptGenerator
from .gitignore import GitignoreManager, GitignoreRule

__all__ = ["PromptGenerator", "GitignoreManager", "GitignoreRule"]
