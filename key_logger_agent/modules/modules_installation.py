import os
import sys
import subprocess
import importlib.util
from logger_config import logger
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_PATH = os.path.join(CONFIG_DIR, "..", "requirements.txt")

def is_package_installed(package_name: str) -> bool:
    return importlib.util.find_spec(package_name) is not None

def is_inside_virtualenv() -> bool:
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def install_package(package_name: str) -> None:
    logger.info(f"🔹 Installing {package_name}...")

    try:
        if is_inside_virtualenv():
            # If inside venv, install within the virtual environment
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        else:
            # If not in venv, install globally (no warning)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package_name])

        logger.info(f"✅ {package_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install {package_name}: {e}")

def install_missing_packages_from_requirements(requirements_file: str = REQUIREMENTS_PATH) -> None:
    if not os.path.exists(requirements_file):
        logger.error(f"❌ Requirements file '{requirements_file}' not found.")
        return

    with open(requirements_file, "r", encoding="utf-8") as file:
        packages = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

    for package in packages:
        if not is_package_installed(package):
            install_package(package)
        else:
            logger.debug(f"✅ {package} is already installed.")
