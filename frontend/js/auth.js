(function () {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value;
      try {
        await window.api.auth.login(username, password);
        location.href = "./user-dashboard.html";
      } catch (err) {
        const msg = err?.response?.data?.detail || "Login failed";
        alert(msg);
      }
    });
  }

  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const errBox = document.getElementById("regError");
      if (errBox) {
        errBox.classList.add("hidden");
        errBox.textContent = "";
      }
      const payload = {
        username: document.getElementById("username").value.trim(),
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value,
        role: document.getElementById("role").value,
      };
      const password2 = document.getElementById("password2")?.value;
      if (password2 != null && payload.password !== password2) {
        if (errBox) {
          errBox.textContent = "Passwords do not match";
          errBox.classList.remove("hidden");
        }
        return;
      }
      try {
        await window.api.auth.register(payload);
        alert("Registered. Please login.");
        location.href = "./login.html";
      } catch (err) {
        const data = err?.response?.data;
        const msg =
          typeof data === "object"
            ? JSON.stringify(data)
            : data || "Registration failed";
        if (errBox) {
          errBox.textContent = msg;
          errBox.classList.remove("hidden");
        } else {
          alert(msg);
        }
      }
    });
  }
})();
