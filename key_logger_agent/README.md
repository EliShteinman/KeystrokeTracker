# 🛠️ Key Logger Agent

A lightweight and configurable key logger for educational and security analysis purposes.

🚨 **WARNING:** This project is for educational use only. Unauthorized use of a key logger may violate laws and policies.

---

## 🚀 Features
✔ Logs keystrokes on macOS and Windows
✔ Supports multiple storage options (console, file, HTTP API)
✔ Configurable encryption methods
✔ Easy installation and setup

---

## 📌 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/Hackathon_KeyLogger.git
cd Hackathon_KeyLogger/key_logger_agent
```

2️⃣ Set Up Virtual Environment (Optional but Recommended)

```sh
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate    # On Windows
```
3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
4️⃣ Create .env Configuration File
```sh
cp example.env .env
```
🔹 Edit .env as needed before running the script.

---

🔧 Configuration

Modify the .env file to customize the agent’s behavior:

```ini
# Encryption key (used for XOR encryption)
DEFAULT_KEY = "CHANGEME_Use_A_Strong_Key"

# Time interval for logging (in seconds)
TIMER_INTERVAL = 30

# Set `True` for testing mode (prints logs instead of storing)
TESTING_MODE = True  # Options: True, False

# Logging configuration
LOG_FILE = key_logger_agent.log
LOG_LEVEL = DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = %(asctime)s - %(levelname)s - %(message)s

# Run duration in seconds (leave empty to run indefinitely)
# RUN_DURATION=120

# Storage options
DATA_FILE = data.json
API_URL = http://127.0.0.1:6000/api/upload
API_RETRIES = 3
API_TIMEOUT = 5

# Choose storage type: "print", "file", "http"
STORAGE_TYPE = file

# Choose encryption type: "xor" or "test"
ENCRYPTION_TYPE = xor
```

▶️ Running the Agent

Run Normally

```sh
python main.py
```
Run in Testing Mode (Prints Logs Instead of Storing)
```sh
python main.py --testing
```

---

🛠️ Troubleshooting

❌ Missing .env file?
✔ Run:
```sh
cp example.env .env
```
❌ Module not found?
✔ Run:
```sh
pip install -r requirements.txt
```
❌ Permission issues on macOS?
✔ Try running with sudo:
```sh
sudo python main.py
```

---

🛡️ Legal Disclaimer

⚠️ Use responsibly. This tool is provided only for ethical use such as security analysis, ethical hacking training, and personal monitoring with consent.

Unauthorized use of key logging software may be illegal in your jurisdiction.

---

## 👥 Contributors

See the full list of contributors in the [CONTRIBUTORS.md](../CONTRIBUTORS.md) file.

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](../LICENSE) file for details.

---

## 📂 Project Structure
```
key_logger_agent/           # 🎯 The main keylogger agent
  ├── modules/              # 📦 Internal modules
  │   ├── __init__.py       # 🛠️ Marks the folder as a Python package
  │   ├── data_sink.py      # 💾 Handles data storage (file, print, HTTP)
  │   ├── decryptor.py      # 🔓 Handles data decryption (if needed)
  │   ├── encryption.py     # 🔒 Encryption logic for stored data
  │   ├── key_logger_manager.py  # 🎯 Manages keylogging logic
  │   ├── key_logger_service.py  # ⌨️ OS-specific key logging implementation
  │   ├── modules_installation.py  # 🔄 Installs missing Python packages
  ├── .env                  # 🌍 Environment variables (ignored by Git)
  ├── example.env           # 📌 Example `.env` file for configuration
  ├── config.py             # ⚙️ Configuration settings (loads `.env`)
  ├── logger_config.py      # 📜 Logger setup and configuration
  ├── main.py               # 🚀 Main script to start the keylogger
  ├── README.md             # 📖 Documentation for key_logger_agent
  ```
