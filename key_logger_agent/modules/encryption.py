from abc import ABC, abstractmethod
from config import Config

class Encryption(ABC):
    @abstractmethod
    def encryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        pass

    @abstractmethod
    def decryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        pass

class XorEncryption(Encryption):
    def encryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        key_bytes = key.encode("utf-8")
        data_bytes = data.encode("utf-8")
        encrypted = bytes([data_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data_bytes))])
        return encrypted.hex()

    def decryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        encrypted_bytes = bytes.fromhex(data)
        key_bytes = key.encode("utf-8")
        decrypted = bytes([encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])
        return decrypted.decode(errors="ignore")

class TestEncryption(Encryption):
    def encryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        return data  # ✅ מצב בדיקה – אין הצפנה אמיתית

    def decryption(self, data: str, key: str = Config.DEFAULT_KEY) -> str:
        return data  # ✅ מצב בדיקה – אין פענוח אמיתי
