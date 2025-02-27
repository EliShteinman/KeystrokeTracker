const API_URL = 'https://kodcode.shteinman.co.uk/api';

/**
 * פונקציה שבודקת אם התשובה מהשרת מעידה על טוקן לא תקין.
 * במקרה שהתשובה היא 401 (או שגיאה דומה), נבצע ניתוק ונפנה לעמוד הלוגין.
 */
// בדיקת התחברות
if (sessionStorage.getItem("loggedIn") !== "true") {
    window.location.href = "/login";
}
function checkTokenValidity(response) {
    if (response.status === 401) {
        // במקרה זה נניח שהטוקן לא תקין או שפג תוקפו
        alert("הטוקן אינו תקין או שפג תוקפו. אנא התחבר מחדש.");
        disconnectUser();
        return false;
    }
    return true;
}

/**
 * פונקציה לניתוק משתמש.
 * מנקה את פרטי ההתחברות (loggedIn, token) ומפנה לדף הלוגין.
 */
function disconnectUser() {
    sessionStorage.removeItem("loggedIn");
    sessionStorage.removeItem("token");
    localStorage.removeItem("token");
    localStorage.removeItem("loggedIn");
    window.location.href = "/login";
}

/**
 * פונקציה להוספת משתמש.
 */
async function addUser(username, password) {
    const token = localStorage.getItem("token");
    try {
        const response = await fetch(`${API_URL}/users/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ username, password })
        });

        // בדיקת תקינות הטוקן
        if (!checkTokenValidity(response)) return;

        const data = await response.json();
        if (response.ok) {
            alert("משתמש נוסף בהצלחה: " + data.message);
            loadUsers(); // רענון הרשימה לאחר הוספה
        } else {
            alert("שגיאה בהוספת משתמש: " + data.error);
        }
    } catch (error) {
        console.error("Error adding user:", error);
    }
}

/**
 * פונקציה לטעינת רשימת המשתמשים.
 */
async function loadUsers() {
    const token = localStorage.getItem("token");
    try {
        const response = await fetch(`${API_URL}/users/list`, { // נניח שיש endpoint כזה
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        // בדיקת תקינות הטוקן
        if (!checkTokenValidity(response)) return;

        const data = await response.json();
        if (response.ok) {
            const userListEl = document.getElementById("user-list");
            userListEl.innerHTML = "";
            data.users.forEach(user => {
                const li = document.createElement("li");
                li.textContent = `שם משתמש: ${user.username}`;
                userListEl.appendChild(li);
            });
        } else {
            alert("שגיאה בטעינת המשתמשים: " + data.error);
        }
    } catch (error) {
        console.error("Error loading users:", error);
    }
}

/**
 * פונקציה לעדכון סיסמה למשתמש.
 */
async function updateUserPassword(username, newPassword) {
    const token = localStorage.getItem("token");
    try {
        const response = await fetch(`${API_URL}/users/${username}`, {
            method: "PUT", // נניח ששיטת העדכון היא PUT
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ password: newPassword })
        });

        // בדיקת תקינות הטוקן
        if (!checkTokenValidity(response)) return;

        const data = await response.json();
        if (response.ok) {
            alert("סיסמה עודכנה בהצלחה: " + data.message);
            loadUsers();
        } else {
            alert("שגיאה בעדכון סיסמה: " + data.error);
        }
    } catch (error) {
        console.error("Error updating user password:", error);
    }
}

/**
 * פונקציה להסרת משתמש.
 */
async function removeUser(username) {
    const token = localStorage.getItem("token");
    try {
        const response = await fetch(`${API_URL}/users/${username}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        // בדיקת תקינות הטוקן
        if (!checkTokenValidity(response)) return;

        const data = await response.json();
        if (response.ok) {
            alert("משתמש הוסר בהצלחה: " + data.message);
            loadUsers();
        } else {
            alert("שגיאה בהסרת משתמש: " + data.error);
        }
    } catch (error) {
        console.error("Error removing user:", error);
    }
}

// מאזינים לטפסים
document.getElementById("add-user-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const username = document.getElementById("add-username").value;
    const password = document.getElementById("add-password").value;
    addUser(username, password);
});

document.getElementById("remove-user-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const username = document.getElementById("remove-username").value;
    removeUser(username);
});

document.getElementById("update-user-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const username = document.getElementById("update-username").value;
    const newPassword = document.getElementById("new-password").value;
    updateUserPassword(username, newPassword);
});

document.getElementById("load-users-button").addEventListener("click", function() {
    loadUsers();
});

// מאזין לכפתור ניתוק המשתמש
document.getElementById("disconnect-button")?.addEventListener("click", disconnectUser);
