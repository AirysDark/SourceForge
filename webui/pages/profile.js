// webui/pages/profile.js

import { apiGet, clearToken } from "../api.js";
import { navigate } from "../core/router.js";

export async function profilePage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Profile</h2>
      <div class="dim">Loading profile...</div>
    </div>
  `;

  try {

    const user = await apiGet("/auth/me");

    content.innerHTML = `
      <div class="card">
        <h2>Profile</h2>

        <div style="display:flex;flex-direction:column;gap:8px;margin-top:12px;">
          <div><strong>Username:</strong> ${user.username}</div>
          <div><strong>Role:</strong> 
            <span class="badge">${user.role}</span>
          </div>
          <div><strong>User ID:</strong> ${user.id}</div>
        </div>

        <div style="margin-top:16px;">
          <button id="logoutBtn">Logout</button>
        </div>
      </div>
    `;

    content.querySelector("#logoutBtn").onclick = () => {
      clearToken();
      navigate("/login");
    };

  } catch (err) {
    console.error(err);

    content.innerHTML = `
      <div class="card">
        <h2>Profile</h2>
        <div class="dim">Unable to load profile.</div>
      </div>
    `;
  }
}