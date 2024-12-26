# API ドキュメント

## PromptGenerator

プロジェクトファイルからAIプロンプトを生成するメインクラスです。

### コンストラクタ

```python
def __init__(self, base_dir: str, file_patterns: List[str], exclude_dirs: List[str] = None)
```

#### パラメータ
- `base_dir`: ファイルを検索する基準ディレクトリ
- `file_patterns`: 含めるファイルパターン（拡張子または完全なファイル名）のリスト
- `exclude_dirs`: 除外するディレクトリのリスト（オプション）

#### 例外
- `NotADirectoryError`: base_dirが存在しないか、ディレクトリでない場合
- `ValueError`: file_patternsが空の場合

### メソッド

#### collect_files
```python
def collect_files(self) -> Dict[str, str]
```
指定されたパターンに一致するファイルを収集します。

戻り値:
- ファイルパスとその内容をマッピングした辞書

使用例:
```python
generator = PromptGenerator(
    base_dir="./my_project",
    file_patterns=[".py", ".js"]
)
files = generator.collect_files()
```

#### generate_prompt
```python
def generate_prompt(self, files_content: Dict[str, str]) -> str
```
収集したファイルからAIプロンプトを生成します。

パラメータ:
- `files_content`: ファイルパスとその内容をマッピングした辞書

戻り値:
- 生成されたプロンプトテキスト

使用例:
```python
prompt = generator.generate_prompt(files)
print(prompt)
```

## GitignoreManager

ファイル除外のための.gitignoreルールを処理するクラスです。

### コンストラクタ

```python
def __init__(self, base_dir: str)
```

#### パラメータ
- `base_dir`: .gitignoreファイルを検索する基準ディレクトリ

使用例:
```python
manager = GitignoreManager("./my_project")
```

### メソッド

#### is_ignored
```python
def is_ignored(self, path: str) -> bool
```
パスが.gitignoreルールによって無視されるべきかをチェックします。

パラメータ:
- `path`: チェックするパス

戻り値:
- パスが無視されるべき場合はTrue

使用例:
```python
if manager.is_ignored("path/to/file.pyc"):
    print("このファイルは無視されます")
```

## 実装例

### 基本的な使用方法
```python
from promptgen import PromptGenerator

# ジェネレーターの初期化
generator = PromptGenerator(
    base_dir="./my_project",
    file_patterns=[".py", ".js"],
    exclude_dirs=["node_modules"]
)

# ファイルの収集
files = generator.collect_files()

# プロンプトの生成
prompt = generator.generate_prompt(files)
print(prompt)
```

### エラーハンドリング
```python
try:
    generator = PromptGenerator(
        base_dir="/non/existent/path",
        file_patterns=[".py"]
    )
except NotADirectoryError as e:
    print(f"ディレクトリエラー: {e}")

try:
    generator = PromptGenerator(
        base_dir=".",
        file_patterns=[]  # 空のパターンリスト
    )
except ValueError as e:
    print(f"バリデーションエラー: {e}")
```

### カスタムファイルパターン
```python
# Dockerファイル関連の収集
generator = PromptGenerator(
    base_dir=".",
    file_patterns=[
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore"
    ]
)

# 設定ファイルの収集
generator = PromptGenerator(
    base_dir=".",
    file_patterns=[
        ".env",
        "config.json",
        "settings.yaml"
    ]
)
```
