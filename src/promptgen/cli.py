"""Command line interface for the promptgen package."""

import argparse
import os
import sys
from typing import List, Optional

from promptgen.generator import PromptGenerator


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: List of command line arguments (used for testing).

    Returns:
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate AI prompts from project files"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Base directory to search (default: current directory)",
    )
    parser.add_argument(
        "--patterns",
        type=str,
        nargs="+",
        default=[
            # 拡張子パターン
            ".py",
            ".js",
            ".ts",
            ".json",
            ".yml",
            ".yaml",
            ".html",
            ".conf",
            ".toml",
            ".md",
            ".css",
            ".scss",
            ".sh",
            # 完全なファイル名パターン
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            ".env",
            ".gitignore",
            "Makefile",
            "requirements.txt",
            "package.json",
            "tsconfig.json",
            ".dockerignore",
        ],
        help="File patterns to include (extensions or complete filenames)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (if not specified, prints to stdout)",
    )
    parser.add_argument(
        "--exclude-dirs",
        type=str,
        nargs="+",
        help="Additional directories to exclude",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Execute the main CLI function.

    Args:
        args: Command line arguments (used for testing).

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        parsed_args = parse_args(args)

        # ディレクトリの存在チェックを追加
        if not os.path.isdir(parsed_args.dir):
            print(f"Error: Directory not found: {parsed_args.dir}", file=sys.stderr)
            return 1

        generator = PromptGenerator(
            base_dir=parsed_args.dir,
            file_patterns=parsed_args.patterns,
            exclude_dirs=parsed_args.exclude_dirs,
        )

        if parsed_args.verbose:
            print(f"Scanning directory: {parsed_args.dir}", file=sys.stderr)
            print(f"File patterns: {parsed_args.patterns}", file=sys.stderr)
            if parsed_args.exclude_dirs:
                print(
                    f"Excluding directories: {parsed_args.exclude_dirs}",
                    file=sys.stderr,
                )

        files_content = generator.collect_files()

        if parsed_args.verbose:
            print(f"Found {len(files_content)} files to process", file=sys.stderr)

        prompt = generator.generate_prompt(files_content)

        if parsed_args.output:
            try:
                with open(parsed_args.output, "w", encoding="utf-8") as f:
                    f.write(prompt)
                if parsed_args.verbose:
                    print(f"Output written to: {parsed_args.output}", file=sys.stderr)
            except IOError as e:
                print(f"Error writing to output file: {str(e)}", file=sys.stderr)
                return 1
        else:
            print(prompt)

        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
