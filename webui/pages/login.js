// webui/pages/login.js

import { apiPost, setToken } from "../api.js";
import { navigate } from "../core/router.js";

export function loginPage(content) {
  content.innerHTML = `
    <div class="card" style="max-width:420px;margin:40px auto;">
      <h2>Login</h2>

      <input id="loginUser" placeholder="Username" />
      <input id="loginPass" type="password" placeholder="Password" />

      <button id="loginBtn">Login</button>

      <div class="dim" style="margin-top:10px;">
        No account? 
        <a href="/register" data-link>Register</a>
      </div>

      <div id="loginMsg" class="dim" style="margin-top:10px;"></div>
    </div>
  `;

  const btn = content.querySelector("#loginBtn");

  btn.onclick = async () => {
    const username = content.querySelector("#loginUser").value.trim();
    const password = content.querySelector("#loginPass").value.trim();
    const msg = content.querySelector("#loginMsg");

    if (!username || !password) {
      msg.textContent = "Username and password required";
      return;
    }

    try {
      const res = await apiPost("/auth/login", { username, password });

      if (!res.access_token) {
        msg.textContent = "Invalid response from server";
        return;
      }

      setToken(res.access_token);

      navigate("/dashboard");

    } catch (err) {
      console.error(err);
      msg.textContent = "Login failed";
    }
  };
}