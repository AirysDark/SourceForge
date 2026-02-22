import { getToken, clearToken } from "../api.js";
import { navigate, getRoute } from "../core/router.js";

export function renderAppShell(root, pageHandler) {

  const currentRoute = getRoute();
  const isAuth = !!getToken();

  root.innerHTML = `
    <div class="layout">
      <aside class="sidebar">
        <div class="logo">SourceForge</div>

        <nav>
          <a href="/dashboard" data-link class="${active("dashboard", currentRoute)}">Dashboard</a>
          <a href="/repos" data-link class="${active("repos", currentRoute)}">Repositories</a>
          <a href="/prs" data-link class="${active("prs", currentRoute)}">Pull Requests</a>
          <a href="/admin" data-link class="${active("admin", currentRoute)}">Admin</a>
          <a href="/profile" data-link class="${active("profile", currentRoute)}">Profile</a>
        </nav>
      </aside>

      <div class="main">
        <div class="topbar">
          <div>Alpha</div>

          <div class="user">
            ${isAuth ? `
              <span>Authenticated</span>
              <button id="logoutBtn" class="logout-btn">Logout</button>
            ` : `
              <span>Guest</span>
            `}
          </div>
        </div>

        <div class="content" id="pageContent"></div>
      </div>
    </div>
  `;

  // Logout handler
  const logoutBtn = root.querySelector("#logoutBtn");
  if (logoutBtn) {
    logoutBtn.onclick = () => {
      clearToken();
      navigate("login");
    };
  }

  // Render page content safely
  const content = root.querySelector("#pageContent");

  try {
    pageHandler(content);
  } catch (err) {
    console.error("Page render error:", err);
    content.innerHTML = `
      <div class="card">
        <h2>Page Error</h2>
        <p>Something went wrong rendering this page.</p>
      </div>
    `;
  }
}

/* Helper for active link highlighting */
function active(name, current) {
  return current.startsWith(name) ? "active" : "";
}