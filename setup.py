# setup.py
from setuptools import setup, find_packages

setup(
    name="promptgen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pathspec>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "isort>=5.0.0",
            "pre-commit>=2.0.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'promptgen=promptgen.cli:main',
        ],
    },
    author="YOUR_NAME",
    author_email="your.email@example.com",
    description="A tool to generate AI prompts from project files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/project-prompt-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)