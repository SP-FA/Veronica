import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]

DEFAULT_MAX_BYTES = 100 * 1024 * 1024
DEFAULT_BACKUP_COUNT = 1
DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


class MultilineAlignFormatter(logging.Formatter):
    """多行日志时，续行左侧补空格，与首行消息正文对齐。

    假定格式串里 ``%(message)s`` 在最后（与 ``DEFAULT_FORMAT`` 一致），否则前缀长度推断可能不准。
    """

    def formatMessage(self, record: logging.LogRecord) -> str:
        # ``Formatter.format`` 已先执行 ``record.message = record.getMessage()``，
        # ``%(message)s`` 读的是 ``record.message``，不能只改 ``record.msg``。
        orig_message = record.message
        try:
            lines = orig_message.splitlines()
            if len(lines) <= 1:
                return super().formatMessage(record)

            record.message = lines[0]
            first = super().formatMessage(record)
            prefix_len = len(first) - len(lines[0])
            if prefix_len < 0:
                prefix_len = 0
            indent = " " * prefix_len
            continuation = "\n".join(indent + line for line in lines[1:])
            return f"{first}\n{continuation}"
        finally:
            record.message = orig_message


def get_logger(
    name: str,
    log_dir: PathLike,
    *,
    log_filename: str = "module.log",
    level: int = logging.DEBUG,
    console: bool = True,
    console_level: int = logging.INFO,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
    fmt: Optional[str] = None,
) -> logging.Logger:
    """为调用模块创建 logger，日志写入 ``log_dir / log_filename``。

    典型用法：``get_logger(__name__, LOGS_DIR, log_filename="vero_email.log")``

    Args:
        name: 一般传入 ``__name__``，便于区分日志来源。
        log_dir: 日志目录（不存在则创建）
        log_filename: 日志文件名。
        level: 文件与 logger 的基准级别（控制台可用 ``console_level`` 单独控制）。
        console: 是否同时输出到 stderr（便于开发时观察）
        console_level: 控制台最低级别。
        max_bytes / backup_count: 滚动日志参数。
        fmt: 自定义格式字符串；默认带时间、级别、logger 名、消息。
    """
    logger = logging.getLogger(name)
    if logger.handlers: return logger

    logger.setLevel(level)
    logger.propagate = False  # 防止日志重复输出

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_filename

    formatter = MultilineAlignFormatter(fmt or DEFAULT_FORMAT)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(console_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
