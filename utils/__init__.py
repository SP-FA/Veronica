from pathlib import Path

from .logger import get_logger
from .configure_util import CfgLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = REPO_ROOT / "logs"
VERO_AUTO_SIGN_LOG_DIR = LOGS_DIR / "vero_auto_sign"
VERO_CHAT_AGENT_LOG_DIR = LOGS_DIR / "vero_chat_agent"
VERO_SUPERVISOR_LOG_DIR = LOGS_DIR / "vero_supervisor"
VERO_EMAIL_LOG_DIR = VERO_CHAT_AGENT_LOG_DIR / "vero_email"
VERO_WECHAT_LOG_DIR = VERO_CHAT_AGENT_LOG_DIR / "vero_wechat"
