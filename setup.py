"""Setup configuration for the promptgen package."""

from setuptools import find_packages, setup

setup(
    name="promptgen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "promptgen": ["py.typed"],
    },
    install_requires=[
        "pathspec>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "flake8-docstrings>=1.7.0",
            "isort>=5.12.0",
            "pre-commit>=3.3.3",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "promptgen=promptgen.cli:main",
        ],
    },
    author="YOUR_NAME",
    author_email="your.email@example.com",
    description="A tool to generate AI prompts from project files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/project-prompt-generator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
)
