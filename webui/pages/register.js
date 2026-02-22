// webui/pages/register.js

import { apiPost } from "../api.js";
import { navigate } from "../core/router.js";

export function registerPage(content) {
  content.innerHTML = `
    <div class="card" style="max-width:420px;margin:40px auto;">
      <h2>Register</h2>

      <input id="regUser" placeholder="Username" />
      <input id="regPass" type="password" placeholder="Password" />

      <button id="regBtn">Create Account</button>

      <div class="dim" style="margin-top:10px;">
        Already have an account? 
        <a href="/login" data-link>Login</a>
      </div>

      <div id="regMsg" class="dim" style="margin-top:10px;"></div>
    </div>
  `;

  const btn = content.querySelector("#regBtn");

  btn.onclick = async () => {
    const username = content.querySelector("#regUser").value.trim();
    const password = content.querySelector("#regPass").value.trim();
    const msg = content.querySelector("#regMsg");

    if (!username || !password) {
      msg.textContent = "Username and password required";
      return;
    }

    try {
      await apiPost("/auth/register", { username, password });

      msg.textContent = "Account created. Redirecting...";
      setTimeout(() => navigate("/login"), 800);

    } catch (err) {
      console.error(err);
      msg.textContent = "Registration failed";
    }
  };
}