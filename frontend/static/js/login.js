document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // מניעת רענון העמוד

    const password = document.getElementById("password").value;
    const usernameElem = document.getElementById("username");
    const username = usernameElem ? usernameElem.value : undefined;
    try {
        const response = await fetch('https://kodcode.shteinman.co.uk/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ password, username }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.token);
            sessionStorage.setItem("loggedIn", "true");
            alert("Login successful!");
            window.location.href = "/";
        } else {
            const errorMessage = await response.text();
            const errorElem = document.getElementById("error-message");
            errorElem.textContent = errorMessage.trim() === "Invalid credentials"
                ? "שם המשתמש או הסיסמה אינם נכונים. אם שכחת את הסיסמה, פנה למנהל המערכת לאיפוס."
                : errorMessage.trim() || "אירעה שגיאה. נסה שוב.";
            errorElem.style.display = "block";
        }
    } catch (error) {
        console.error("Error logging in:", error);
        const errorElem = document.getElementById("error-message");
        errorElem.textContent = "שגיאה בחיבור לשרת. נסה שוב מאוחר יותר.";
        errorElem.style.display = "block";
    }
});