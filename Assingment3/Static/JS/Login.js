document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById("loginForm");
    const errorMessage = document.getElementById("errorMessage");
  
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevent the page from reloading
  
        // Clear any previous error message
        errorMessage.textContent = "";
  
        try {
          // Create a FormData object from the form
          const formData = new FormData(loginForm);
  
          // Send the AJAX POST request using Fetch API
          const response = await fetch(loginForm.action, {
            method: "POST",
            headers: {
              "X-Requested-With": "XMLHttpRequest"  // Marks this as an AJAX request
            },
            body: formData
          });
  
          const data = await response.json();
  
          if (data.status === "error") {
            // Display error message without reloading the page
            errorMessage.textContent = data.message;
            errorMessage.style.color = "red";
          } else if (data.status === "success") {
            // On successful login, redirect to the specified page
            window.location.href = data.redirect;
          }
        } catch (err) {
          console.error("Error during login:", err);
          errorMessage.textContent = "An unexpected error occurred. Please try again.";
          errorMessage.style.color = "red";
        }
      });
    }
  });
  