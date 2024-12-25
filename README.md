# Project Prompt Generator

A Python tool that generates AI prompts by analyzing project files. It respects .gitignore rules and allows custom directory exclusions.

## Features

- Scans project directories for specific file types
- Respects .gitignore rules
- Allows custom directory exclusions
- Supports multiple file patterns
- Generates formatted prompts for AI interactions

## Installation

### From GitHub
```bash
pip install git+https://github.com/YOUR_USERNAME/project-prompt-generator.git
```

### For Development
```bash
git clone https://github.com/YOUR_USERNAME/project-prompt-generator.git
cd project-prompt-generator
pip install -e .
```

## Usage

### Command Line
```bash
promptgen --dir /path/to/project --patterns .py .js --output output.txt
```

### Python API
```python
from promptgen import PromptGenerator

generator = PromptGenerator(
    base_dir="./my_project",
    file_patterns=[".py", ".js"],
    exclude_dirs=["node_modules"]
)
files_content = generator.collect_files()
prompt = generator.generate_prompt(files_content)
print(prompt)
```

## Options

- `--dir`: Base directory to search (default: current directory)
- `--patterns`: File patterns to include (extensions or complete filenames)
- `--output`: Output file path (optional)
- `--exclude-dirs`: Additional directories to exclude
- `--verbose`: Enable verbose output

## Default File Patterns

- Python: `.py`
- JavaScript: `.js`
- TypeScript: `.ts`
- JSON: `.json`
- YAML: `.yml`, `.yaml`
- HTML: `.html`
- Configuration: `.conf`, `.toml`
- Markdown: `.md`
- Stylesheets: `.css`, `.scss`
- Shell Scripts: `.sh`
- Common Project Files:
  - `Dockerfile`
  - `docker-compose.yml`
  - `docker-compose.yaml`
  - `.env`
  - `.gitignore`
  - `Makefile`
  - `requirements.txt`
  - `package.json`
  - `tsconfig.json`
  - `.dockerignore`

## Documentation

- [Requirements Specification](docs/requirements.md)
- [Development Steps](docs/development_steps.md)

## Development

This project uses:
- `black` for code formatting
- `flake8` for code linting
- `isort` for import sorting
- `pytest` for testing

### Setting up development environment

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/project-prompt-generator.git
cd project-prompt-generator
```

2. Install development dependencies
```bash
pip install -e ".[dev]"
```

3. Install pre-commit hooks
```bash
pre-commit install
```

### Running Tests
```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Status

This project is under active development. See the [project board](https://github.com/YOUR_USERNAME/project-prompt-generator/projects/1) for current status.
