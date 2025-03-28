const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("Confirmpassword");
const registerButton = document.getElementById("button");
const validStatement = document.getElementById("p3");
const studentCheck = document.getElementById("StudentLogin");
const instructorCheck = document.getElementById("InstructorLogin");
const nameField = document.getElementById("name");

async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, "0")).join("");
}                         

registerButton.onclick = async function() {
    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const confirmPasswordValue = confirmPassword.value.trim();
    const nameValue = nameField.value.trim();
    const accountType = studentCheck.checked ? "student" : instructorCheck.checked ? "instructor" : null;

    // Validation for missing fields
    if (!usernameValue || !emailValue || !passwordValue || !confirmPasswordValue || !accountType || !nameValue) {
        validStatement.textContent = "Missing Fields";
        validStatement.style.color = "red";
        return;
    }

    // Password confirmation check
    if (passwordValue !== confirmPasswordValue) {
        validStatement.textContent = "Passwords do not match";
        validStatement.style.color = "red";
        return;
    }

    // Hash password (though not saving it anywhere)
    const hashedPassword = await hashPassword(passwordValue);
    console.log("Hashed Password:", hashedPassword); // Just for debugging

    validStatement.textContent = "Successfully Registered!";
    validStatement.style.color = "green";

    // Redirect after 2 seconds
    setTimeout(() => window.location.href = "LoginPage.html", 2000);
};