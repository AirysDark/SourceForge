// webui/components/login.js

import { apiPost, setToken } from "../api.js";
import { navigate } from "../core/router.js";

class SfLogin extends HTMLElement {

  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = `
      <div class="card">
        <h3>Login</h3>
        <input class="u" placeholder="username" autocomplete="username">
        <input class="p" placeholder="password" type="password" autocomplete="current-password">
        <button class="log">Login</button>
        <div class="msg"></div>
      </div>
    `;

    this.querySelector(".log").addEventListener("click", () => this.doLogin());

    // Allow Enter key login
    this.querySelector(".p").addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        this.doLogin();
      }
    });
  }

  async doLogin() {
    const username = this.value(".u");
    const password = this.value(".p");

    if (!username || !password) {
      this.msg("Username and password required");
      return;
    }

    try {
      const res = await apiPost("/auth/login", {
        username,
        password
      });

      if (!res?.access_token) {
        throw new Error("Invalid response");
      }

      setToken(res.access_token);

      this.msg("Logged in");

      // Navigate cleanly
      navigate("dashboard");

    } catch (err) {
      console.error("Login error:", err);
      this.msg("Login failed");
    }
  }

  value(selector) {
    return this.querySelector(selector)?.value?.trim() || "";
  }

  msg(text) {
    const el = this.querySelector(".msg");
    if (el) el.textContent = text;
  }
}

customElements.define("sf-login", SfLogin);