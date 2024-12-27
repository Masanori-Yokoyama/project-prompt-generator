"""Test cases for logging configuration."""

import logging
import sys
from io import StringIO

from promptgen.logging import LOGGER, setup_logging


def test_setup_logging():
    """Test logging setup with different levels."""
    # 標準エラー出力をキャプチャするための設定
    stderr = StringIO()
    old_stderr = sys.stderr
    sys.stderr = stderr

    try:
        # デフォルトレベル（INFO）でのセットアップ
        setup_logging()
        assert LOGGER.level == logging.INFO

        # DEBUGレベルでのセットアップ
        setup_logging("DEBUG")
        assert LOGGER.level == logging.DEBUG

        # WARNINGレベルでのセットアップ
        setup_logging("WARNING")
        assert LOGGER.level == logging.WARNING

        # 無効なレベルでのセットアップ（デフォルトのINFOになるはず）
        setup_logging("INVALID")
        assert LOGGER.level == logging.INFO

        # ログメッセージのテスト
        LOGGER.warning("Test warning message")
        assert "WARNING - Test warning message" in stderr.getvalue()

    finally:
        # 標準エラー出力を元に戻す
        sys.stderr = old_stderr
        # ロガーをクリーンアップ
        LOGGER.handlers.clear()


def test_logger_handlers():
    """Test logger handler configuration."""
    # 既存のハンドラをクリア
    LOGGER.handlers.clear()

    # ロギングのセットアップ
    setup_logging()

    # ハンドラの確認
    assert len(LOGGER.handlers) == 1
    handler = LOGGER.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.stream == sys.stderr

    # フォーマットの確認
    formatter = handler.formatter
    assert formatter._fmt == "%(levelname)s - %(message)s"

    # ロガーをクリーンアップ
    LOGGER.handlers.clear()
