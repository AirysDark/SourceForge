// webui/app.js

import { registerRoute, initRouter, navigate, getRoute } from "./core/router.js";
import { getToken } from "./api.js";
import { renderAppShell } from "./layout/app-shell.js";

/* ===============================
   Pages
================================ */

import { dashboardPage } from "./pages/dashboard.js";
import { repoPage } from "./pages/repo.js";
import { reposPage } from "./pages/repos.js";
import { adminPage } from "./pages/admin.js";
import { prListPage } from "./pages/pr-list.js";
import { profilePage } from "./pages/profile.js";
import { createRepoPage } from "./pages/create-repo.js";
import { createPrPage } from "./pages/create-pr.js";
import { activityPage } from "./pages/activity.js";
import { settingsPage } from "./pages/settings.js";
import { metricsPage } from "./pages/metrics.js";
import { loginPage } from "./pages/login.js";
import { registerPage } from "./pages/register.js";

/* ===============================
   Components
================================ */

import "./components/activity-feed.js";
import "./components/commit-graph.js";
import "./components/commit-list.js";
import "./components/commit-timeline.js";
import "./components/commits-panel.js";
import "./components/diff-viewer.js";
import "./components/fabric-browser.js";
import "./components/fabric-buckets.js";
import "./components/fabric-deep.js";
import "./components/file-tree.js";
import "./components/issues-list.js";
import "./components/issues-panel.js";
import "./components/pr-detail.js";
import "./components/pr-panel.js";
import "./components/repo-code.js";
import "./components/repo-list.js";
import "./components/repo-switcher.js";
import "./components/repo-tree.js";
import "./components/repo-viewer.js";
import "./components/repos.js";
import "./components/search-box.js";
import "./components/search-results.js";
import "./components/theme-check.js";
import "./components/ui.js";
import "./components/virtual-repos.js";

/* ===============================
   Auth Guard
================================ */

function requireAuth(handler) {
  return (root) => {
    if (!getToken()) {
      navigate("/login");
      return;
    }
    renderAppShell(root, handler);
  };
}

/* ===============================
   Dynamic Repo Route
================================ */

function dynamicRepoRoute(root) {
  const route = getRoute();
  const parts = route.split("/");

  if (parts.length === 2 && parts[0] === "repo") {
    renderAppShell(root, (content) => {
      repoPage(content, parts[1]);
    });
    return;
  }

  root.innerHTML = `
    <div class="card">
      <h2>Invalid Repo Route</h2>
    </div>
  `;
}

/* ===============================
   Route Registration
================================ */

/* Public */
registerRoute("login", loginPage);
registerRoute("register", registerPage);

/* Default */
registerRoute("", requireAuth(dashboardPage));

/* Protected */
registerRoute("dashboard", requireAuth(dashboardPage));
registerRoute("repos", requireAuth(reposPage));
registerRoute("repo", requireAuth(dynamicRepoRoute));
registerRoute("admin", requireAuth(adminPage));
registerRoute("prs", requireAuth(prListPage));
registerRoute("profile", requireAuth(profilePage));
registerRoute("create-repo", requireAuth(createRepoPage));
registerRoute("create-pr", requireAuth(createPrPage));
registerRoute("activity", requireAuth(activityPage));
registerRoute("settings", requireAuth(settingsPage));
registerRoute("metrics", requireAuth(metricsPage));

/* ===============================
   Init
================================ */

window.addEventListener("DOMContentLoaded", () => {
  initRouter();
});