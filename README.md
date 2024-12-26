# Project Prompt Generator

プロジェクトファイルを解析してAIプロンプトを生成するPythonツールです。.gitignoreルールを尊重し、カスタムディレクトリの除外にも対応しています。

## 特徴

- 🔍 特定のファイルタイプに対応したプロジェクトディレクトリのスキャン
- 📝 .gitignoreルールの適用
- 🚫 カスタムディレクトリの除外機能
- 🎯 複数のファイルパターンに対応
- 🔄 AI対話用の整形されたプロンプト生成

## インストール

### GitHubからのインストール
```bash
pip install git+https://github.com/Masanori-Yokoyama/project-prompt-generator.git
```

### 開発用インストール
```bash
git clone https://github.com/Masanori-Yokoyama/project-prompt-generator.git
cd project-prompt-generator
pip install -e ".[dev]"
```

## 使用方法

### コマンドラインインターフェース
```bash
# 基本的な使用方法
promptgen --dir /path/to/project

# ファイルパターンの指定
promptgen --dir . --patterns .py .js .json

# ディレクトリの除外
promptgen --dir . --exclude-dirs node_modules dist

# 出力をファイルに保存
promptgen --dir . --output prompt.txt

# 詳細出力の有効化
promptgen --dir . --verbose
```

### Python API
```python
from promptgen import PromptGenerator

# ジェネレーターの初期化
generator = PromptGenerator(
    base_dir="./my_project",
    file_patterns=[".py", ".js"],
    exclude_dirs=["node_modules"]
)

# ファイルの収集とプロンプト生成
files = generator.collect_files()
prompt = generator.generate_prompt(files)
print(prompt)
```

## 設定

### デフォルトのファイルパターン
以下のファイルパターンがデフォルトで含まれています：
- Python: `.py`
- JavaScript: `.js`
- TypeScript: `.ts`
- JSON: `.json`
- YAML: `.yml`, `.yaml`
- HTML: `.html`
- 設定ファイル: `.conf`, `.toml`
- Markdown: `.md`
- スタイルシート: `.css`, `.scss`
- シェルスクリプト: `.sh`
- 一般的なプロジェクトファイル:
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

### コマンドラインオプション
| オプション | 説明 | デフォルト値 |
|------------|------|--------------|
| `--dir` | 検索を開始するディレクトリ | カレントディレクトリ |
| `--patterns` | 含めるファイルパターン | [デフォルトパターン] |
| `--output` | 出力ファイルパス | なし（標準出力） |
| `--exclude-dirs` | 除外するディレクトリ | なし |
| `--verbose` | 詳細出力の有効化 | False |

## 開発

### 開発環境のセットアップ
```bash
# リポジトリのクローン
git clone https://github.com/Masanori-Yokoyama/project-prompt-generator.git
cd project-prompt-generator

# 開発用依存関係のインストール
pip install -e ".[dev]"

# pre-commit hooksのインストール
pre-commit install
```

### テストの実行
```bash
# 全テストの実行
pytest

# カバレッジ付きでテストを実行
pytest --cov=promptgen

# 特定のテストファイルの実行
pytest tests/test_generator.py
```

### コード品質
このプロジェクトでは以下のツールを使用しています：
- `black`: コードフォーマット
- `flake8`: コードリント
- `isort`: インポートの整理
- `mypy`: 型チェック
- `pre-commit`: Gitフック

### 型ヒント
このプロジェクトは完全に型付けされており、`py.typed`マーカーファイルを含んでいます。IDEとの統合はそのまま機能します。

## 貢献

貢献は歓迎します！プルリクエストを気軽に提出してください。

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. テストを実行し、パスすることを確認
4. 変更をコミット（`git commit -m '素晴らしい機能を追加'`）
5. ブランチにプッシュ（`git push origin feature/amazing-feature`）
6. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。
