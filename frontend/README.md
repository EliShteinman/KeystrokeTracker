# 🎨 **Flask Keylogger Frontend**

### **📚 Overview**
This is a **Flask-based frontend** for the Keylogger project, developed as part of a **final college project**.

The interface displays logs and provides user management features using **HTML, CSS, and JavaScript**.

---

## 📂 **Project Structure**

```
frontend/                     # 🎨 Frontend project directory
  ├─ static/                 # 📂 Static files (CSS, JS, Images)
  │   ├─ css/                # 🎨 Stylesheets
  │   │   ├─ style.css       # 🖌️ Main CSS file
  │   ├─ images/             # 🖼️ Images (logos, backgrounds, etc.)
  │   ├─ js/                 # 📝 JavaScript logic files
  │   │   ├─ index.js        # 🏠 Script for the main page
  │   │   ├─ login.js        # 🔑 Handles login functionality
  │   │   └─ user_management.js  # 👤 Manages user-related actions
  ├─ templates/              # 📂 HTML Templates
  │   ├─ index.html          # 🏠 Homepage
  │   ├─ login.html          # 🔑 Login page
  │   └─ user_management.html  # 👤 User management page
  ├─ app.py                  # 🚀 Main Flask application
  ├─ README.md               # 📚 Project documentation
  └─ requirements.txt        # 📦 Required Python packages
```

🔹 **`templates/`** – Contains HTML files used for rendering pages.
🔹 **`static/`** – Includes **CSS, JavaScript, and image files**.
🔹 **`app.py`** – The main **Flask** file that runs the server and handles requests.
🔹 **`requirements.txt`** – Lists the dependencies required to run the project.

---

## 🚀 **Installation & Setup**

### **1️⃣ Install Dependencies**
Ensure you have **Python** installed, then run:
```sh
pip install -r requirements.txt
```

### **2️⃣ Start the Flask Server**
```sh
python app.py
```
🔹 **By default, the server runs at:** [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/)

---

## 🛠 **Main Features**

The Flask application (`app.py`) handles the following routes:
- **`/`** → Homepage (`index.html`)
- **`/login`** → Login page (`login.html`)
- **`/user-management`** → User management interface (`user_management.html`)

---

## 🛠 **Development & Customization**

1️⃣ **Modify the Styling**
- Edit `static/css/style.css` to change the UI appearance.

2️⃣ **Update JavaScript Behavior**
- Add or modify scripts in `static/js/*.js` to enhance interactivity.

---

## 📝 **License**
This project is licensed under the **MIT License**.
See the full license details in the [LICENSE](../LICENSE) file.

---

## 👤 **Contributors**
See the full list of contributors in the [CONTRIBUTORS.md](../CONTRIBUTORS.md) file.

---

## 🛡 **Legal Disclaimer**
🚨 **Use this project responsibly and in compliance with local laws.**
Unauthorized use of keylogging software **may be illegal** in your jurisdiction.

---

🚀 **The README is now updated and ready for the project!** 🎯

