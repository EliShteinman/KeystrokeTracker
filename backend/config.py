import os
from dotenv import load_dotenv
import argparse

# ================================
# קביעת נתיב לתיקיית הקונפיג, הקובץ .env ותיקיית הנתונים (KEYSTROKES_DIR)
# ================================
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CONFIG_DIR, ".env")
# נתיב לתיקיית הנתונים שבה יאוחסנו נתוני ההקלדות (KEYSTROKES)
KEYSTROKES_DIR_DEFAULT = os.path.join(CONFIG_DIR, "data")

# בדיקה שהקובץ .env קיים, אחרת להודיע על שגיאה.
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError("[ERROR] Missing `.env` file! Please create one using `.env.example`.")

# ================================
# ניתוח ארגומנטים מהשורה (CLI arguments)
# ================================
parser = argparse.ArgumentParser(description="Run the keylogger script.")
parser.add_argument("--testing", action="store_true", help="Run in testing mode.")
args = parser.parse_args()

# ================================
# הגדרת אפשרויות לוג (Logging)
# ================================
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

# ================================
# טעינת משתני סביבה מהקובץ .env
# ================================
load_dotenv()

# ================================
# מחלקת קונפיגורציה ראשית
# ================================
class Config:
    # הגדרות Flask:
    FLASK_ENV: str = os.getenv("FLASK_ENV", "production")
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")

    # הגדרות CORS:
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS", "*")

    # הגדרות Logging:
    DEFAULT_KEY: str = os.getenv("DEFAULT_KEY", "")
    LOG_FILE: str = os.getenv("LOG_FILE", "backend.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    if LOG_LEVEL not in VALID_LOG_LEVELS:
        raise ValueError(f"[ERROR] Invalid LOG_LEVEL '{LOG_LEVEL}'. Choose from: {', '.join(VALID_LOG_LEVELS)}")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")

    # הגדרות מצב בדיקה (Testing):
    TESTING_MODE: bool = args.testing or os.getenv("TESTING_MODE", "False").lower() == "true"

    # הגדרות נתוני ההקלדות:
    # KEYSTROKES_DIR - הנתיב לתיקיית הנתונים שבה יאוחסנו כל נתוני ההקלדות.
    # ניתן לשנות זאת דרך משתנה סביבה (KEYS_FOLDER) או להשתמש בערך ברירת מחדל.
    KEYSTROKES_DIR: str = os.getenv("KEYS_FOLDER", KEYSTROKES_DIR_DEFAULT)

    # הגדרות JWT:
    JWT_SECRET: str = os.getenv("JWT_SECRET", 'your_secret_key')
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", 'HS256')

    # רשימת המשתמשים (למטרות הדגמה בלבד – מומלץ להעביר לניהול חיצוני)
    VALID_USERS = [
        {"username": "user1", "password": "123"},
        {"username": "user2", "password": "456"},
    ]
