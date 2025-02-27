import os
import sys
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict, Callable, TypeVar, Union, Tuple, cast
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from functools import wraps

# הוספת הנתיב של המודולים (Upload, StrokesByDate)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.upload import Upload
from backend.modules.strokes_by_machine import StrokesByMachine
from config import Config

# ================================
# הגדרות בסיסיות ופרמטרים
# ================================
# F - טיפוס פונקציה שמחזירה תגובה (Response) או תגובה עם קוד סטטוס
F = TypeVar("F", bound=Callable[..., Union[Response, Tuple[Response, int]]])

# ================================
# אתחול Flask והגדרות CORS
# ================================
app = Flask(__name__)
# טעינת ההגדרות מ־Config (כולל נתיבי נתונים, JWT, הגדרות Flask וכו')
app.config.from_object(Config)
debug_mode: bool = str(app.config.get("FLASK_DEBUG", "0")).lower() in ("1", "true", "yes")
# הגדרת CORS לפי הדומיינים המורשים שמוגדרים ב־Config
CORS(app, supports_credentials=True, resources={r"/*": {"origins": app.config["CORS_ALLOWED_ORIGINS"]}})

# ================================
# Endpoint - Login
# ================================
# ראוט זה מטפל בבקשות התחברות.
# הנתונים מתקבלים כ-JSON, ובודקים מול רשימת המשתמשים המוגדרת ב־Config.
# במקרה שהפרטים נכונים, מייצרים טוקן JWT עם תוקף של שעה.
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if data and data.get("username") and data.get("password"):
            username = data.get("username")
            password = data.get("password")
            # בדיקת תקינות הנתונים מול המשתמשים המוגדרים ב־Config
            valid = any(user["username"] == username and user["password"] == password for user in Config.VALID_USERS)
            if valid:
                payload: Dict[str, Any] = {
                    "user": username,
                    "exp": datetime.now(timezone.utc) + timedelta(hours=1)
                }
                token: str = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
                return jsonify({"message": "Login successful", "user": username, "token": token}), 200
        return "Invalid credentials", 401
    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return f"Internal Server Error: {e}", 500

# ================================
# Decorator - בדיקת Token
# ================================
# דקורטור זה מוודא את תקינות טוקן ה־JWT לפני גישה לראוטים מוגנים.
# במידה והטוקן חסר, לא תקין או פג תוקף – מוחזרת שגיאה מתאימה.
def token_required(f: F) -> F:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Union[Response, Tuple[Response, int]]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing!"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid token format!"}), 401

        token = parts[1]
        try:
            jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except Exception:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(*args, **kwargs)
    return cast(F, decorated)

# ================================
# Endpoint - העלאת נתונים (ללא אימות)
# ================================
# ראוט זה מאפשר העלאת נתונים ללא צורך באימות.
# הנתונים מתקבלים כ-JSON ומועברים למחלקת Upload לטיפול נוסף.
@app.route('/api/upload', methods=['POST'])
def upload() -> Response:
    data: dict[str, Any] = request.get_json()
    if not data:
        response = jsonify({"error": "No JSON data provided"})
        response.status_code = 400
        return response
    upload_instance = Upload(data)
    return upload_instance.upload()

# ================================
# Endpoint - שליפת רשימת מכונות (מוגן ב-token)
# ================================
# ראוט זה מחזיר רשימה של קבצי לוג (כל אחד מייצג מכונה) הנמצאים בתיקיית KEYSTROKES_DIR המוגדרת ב־Config.
# ראוט זה מוגן באמצעות הדקורטור token_required.
@app.route('/api/machine', methods=['GET'])
@token_required
def get_target_machines_list() -> Response:
    if not os.path.exists(Config.KEYSTROKES_DIR):
        response = jsonify([])  # במקרה שאין קבצים, מוחזרת רשימה ריקה
        response.status_code = 200
        return response
    machine_list: List[Dict[str, Any]] = [
        {
            "id": idx + 1,
            "name": file_name.replace("computer_", "").replace("_logs.csv", "")
        }
        for idx, file_name in enumerate(os.listdir(Config.KEYSTROKES_DIR))
        if file_name.endswith("_logs.csv")
    ]
    response = jsonify(machine_list)
    response.status_code = 200
    return response

# ================================
# Endpoint - שליפת נתוני הקשות לפי מכונה (מוגן ב-token)
# ================================
# ראוט זה מקבל מזהה של מכונה כפרמטר ומחזיר את נתוני ההקלדות (strokes) עבור אותה מכונה,
# באמצעות מחלקת StrokesByMachine.
@app.route('/api/machine/<machine_id>', methods=['GET'])
@token_required
def get_target_machine_strokes_by_machine(machine_id: str) -> Response:
    if not machine_id:
        response = jsonify({"error": "No target machine provided"})
        response.status_code = 400
        return response
    machine_strokes = StrokesByMachine(machine_id)
    return machine_strokes.get_data()

# ================================
# Endpoint - הוספת משתמש (מוגן ב-token)
# ================================
# ראוט זה מאפשר הוספת משתמש חדש למערכת.
# הנתונים מתקבלים כ-JSON, ובודקים אם המשתמש כבר קיים לפני ההוספה.
# (בהערה – מומלץ להעביר ניהול משתמשים למסד נתונים או מערכת חיצונית)
@app.route("/api/users/add", methods=["POST"])
@token_required
def add_user():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400
    username = data.get("username")
    password = data.get("password")
    # בדיקה האם המשתמש כבר קיים
    if any(user["username"] == username for user in Config.VALID_USERS):
        return jsonify({"error": "User already exists"}), 400
    Config.VALID_USERS.append({"username": username, "password": password})
    return jsonify({"message": f"User {username} added successfully"}), 200


# ================================
# Endpoint - הצגת רשימת משתמשים (מוגן ב-token)
# ================================
# ראוט זה מחזיר רשימה של המשתמשים הקיימים במערכת.
@app.route("/api/users/list", methods=["GET"])
@token_required
def list_users():
    # נחזיר את המשתמשים ללא סיסמאות לשם פרטיות (במידה וזה רלוונטי)
    users = [{"username": user["username"]} for user in Config.VALID_USERS]
    return jsonify({"users": users}), 200


# ================================
# Endpoint - עדכון סיסמה למשתמש (מוגן ב-token)
# ================================
# ראוט זה מאפשר לעדכן את הסיסמה של משתמש קיים.
# הנתונים מתקבלים כ-JSON הכוללים את הסיסמה החדשה.
@app.route("/api/users/<username>", methods=["PUT"])
@token_required
def update_user_password(username: str):
    data = request.get_json()
    if not data or not data.get("password"):
        return jsonify({"error": "Missing new password"}), 400
    new_password = data.get("password")
    for user in Config.VALID_USERS:
        if user["username"] == username:
            user["password"] = new_password
            return jsonify({"message": f"Password for user {username} updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404


# ================================
# Endpoint - הסרת משתמש (מוגן ב-token)
# ================================
# ראוט זה מאפשר הסרת משתמש קיים מהמערכת לפי שם המשתמש.
# במקרה שהמשתמש לא נמצא, מוחזרת הודעת שגיאה.
@app.route("/api/users/<username>", methods=["DELETE"])
@token_required
def remove_user(username: str):
    for user in Config.VALID_USERS:
        if user["username"] == username:
            Config.VALID_USERS.remove(user)
            return jsonify({"message": f"User {username} removed successfully"}), 200
    return jsonify({"error": "User not found"}), 404

# ================================
# הפעלת השרת
# ================================
# הפעלת האפליקציה על כתובת ופורט מוגדרים, תוך שימוש בהגדרת debug מה־Config
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=debug_mode)
