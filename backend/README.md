# Keylogger Backend

This project provides a Flask-based backend for handling keystroke logs from multiple computers. It supports receiving encrypted log data, decrypting it, and storing it in CSV files, as well as retrieving and filtering the data.

## Requirements

- Python 3.9+ (recommended)
- Flask
- Pandas
- Any other dependencies listed in `requirements.txt`

Install the dependencies:

```bash
pip install -r requirements.txt
python3 app.py

Project Structure

backend/
  ├── modules/
  │    ├── encryption.py
  │    └── ...
  ├── app.py
  ├── requirements.txt
  └── README.md

	•	app.py: Main Flask application containing all endpoints.
	•	encryption.py: Contains the encryption/decryption logic.
	•	requirements.txt: List of Python dependencies.
	•	README.md: Project documentation.

Running the Server

cd backend
python3 app.py  # or python -m backend.app, depending on your setup

By default, the server runs at http://0.0.0.0:6000.

Endpoints

1. /api/upload (POST)
	•	Description: Receives a JSON payload with log data from a computer, decrypts it, and appends it to a CSV file (creates a header row if the file is new).
	•	Expected JSON:

{
  "computer_name": "machine1",
  "timestamp": "2025-02-22 14:30",
  "encrypted_data": "Encrypted content",
  "encryption_key": "secret"
}


	•	Response:

{
  "status": "success",
  "file_path": "data/computer_machine1_logs.csv"
}



2. /api/get_target_machine_list (GET)
	•	Description: Returns a list of all computers (based on CSV files in the data folder).
	•	Response:

{
  "machines": ["machine1", "machine2"]
}



3. /api/get_keystrokes (GET)
	•	Description: Returns the overall date range (min and max) available for a specific computer’s logs.
	•	Query Param:
	•	target_machine: Name of the computer (e.g. machine1).
	•	Response:

{
  "min_date": "2025-02-22 13:00",
  "max_date": "2025-02-23 08:45"
}



4. /api/get_keystrokes_by_date (GET)
	•	Description: Returns filtered keystrokes for a specific computer in a given date range, with optional modes for returning data.
	•	Query Params:
	•	target_machine: Name of the computer.
	•	start_date: Start of date range (e.g. 2025-02-22 00:00).
	•	end_date: End of date range (e.g. 2025-02-23 23:59).
	•	mode (optional): "text" to return the keystrokes as a concatenated string, or "table" (default) to return them in tabular form.
	•	Example Response (mode=“text”):

{
  "keystrokes": "some text\nanother line"
}


	•	Example Response (mode=“table”):

{
  "data": [
    {
      "year": 2025,
      "month": 2,
      "day": 22,
      "hour": 14,
      "minute": 30,
      "decrypted_data": "some text"
    },
    ...
  ]
}



Notes
	•	The data folder is set to data by default. Make sure it exists or that the app has permissions to create it.
	•	Encryption/Decryption logic is handled in modules/encryption.py.
	•	These endpoints have not been fully tested; please test and adjust as needed.

License

(If applicable, add license details or disclaimers here.)
