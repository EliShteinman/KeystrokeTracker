from abc import ABC, abstractmethod
import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from logger_config import logger
from config import Config


class DataSink(ABC):
    @abstractmethod
    def storage(self, data: dict[str, str]) -> None:
        pass

class FileSink(DataSink):
    def __init__(self, filename: str = Config.DATA_FILE ) -> None:
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False)

    def storage(self, data: dict[str, str]) -> None:
        with open(self.filename, "r+", encoding="utf-8") as file:
            try:
                file_content = json.load(file)
            except json.JSONDecodeError:
                file_content: list[dict[str,str]] = []

            # הוספת המידע החדש לרשימה הקיימת
            file_content.append(data)

            # החזרת מצביע הקובץ לתחילתו
            file.seek(0)
            # כתיבה מחודשת של הרשימה כ-JSON עדכני
            json.dump(file_content, file, indent=4, ensure_ascii=False)
            # במקרה שיש תוכן בקובץ מעבר לאורך הרשימה החדשה - נחתוך
            file.truncate()

class PrintSink(DataSink):

    def storage(self, data: dict[str, str]) -> None:
        print(data)

class HttpSink(DataSink):
    def __init__(self) -> None:
        self.url = Config.API_URL
        self.session = requests.Session()
        retries = Retry(
            total=Config.API_RETRIES,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def storage(self, data: dict[str, str]) -> None:
        headers = {'Content-Type': 'application/json'}
        try:
            response = self.session.post(self.url, json=data, headers=headers, timeout=Config.API_TIMEOUT)
            response.raise_for_status()
            logger.info(f"Success: {response.json()}")
        except requests.exceptions.HTTPError as e:
            logger.info(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            logger.info("Connection failed: Server might be down.")
        except requests.exceptions.Timeout:
            logger.info("Request timed out: Server took too long to respond.")
        except requests.exceptions.RequestException as e:
            logger.info(f"Unexpected error: {e}")
