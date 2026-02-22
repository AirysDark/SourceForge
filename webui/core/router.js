// webui/core/router.js

import { getToken } from "../api.js";

const routes = [];

/* ============================================
   Register Route
============================================ */

export function registerRoute(path, handler) {
  routes.push({ path: normalize(path), handler });
}

/* ============================================
   Utilities
============================================ */

function normalize(path) {
  if (!path) return "";

  path = path.split("?")[0];

  if (path.startsWith("/")) path = path.slice(1);
  if (path.endsWith("/")) path = path.slice(0, -1);

  return path;
}

export function getRoute() {
  return normalize(location.pathname);
}

export function getQuery() {
  const query = {};
  const search = location.search.slice(1);
  if (!search) return query;

  search.split("&").forEach(pair => {
    const [k, v] = pair.split("=");
    query[decodeURIComponent(k)] = decodeURIComponent(v || "");
  });

  return query;
}

export function navigate(path, replace = false) {
  if (!path.startsWith("/")) path = "/" + path;

  if (replace) {
    history.replaceState({}, "", path);
  } else {
    history.pushState({}, "", path);
  }

  render();
}

/* ============================================
   Route Matching
============================================ */

function matchRoute(route) {
  const routeParts = route.split("/");

  // Exact match first
  for (const r of routes) {
    if (r.path === route) {
      return { handler: r.handler, params: {} };
    }
  }

  // Dynamic match
  for (const r of routes) {
    const pathParts = r.path.split("/");

    if (pathParts.length !== routeParts.length) continue;

    let params = {};
    let matched = true;

    for (let i = 0; i < pathParts.length; i++) {
      if (pathParts[i].startsWith(":")) {
        params[pathParts[i].slice(1)] = routeParts[i];
      } else if (pathParts[i] !== routeParts[i]) {
        matched = false;
        break;
      }
    }

    if (matched) {
      return { handler: r.handler, params };
    }
  }

  return null;
}

/* ============================================
   Render
============================================ */

let rendering = false;

function render() {
  if (rendering) return;
  rendering = true;

  const root = document.getElementById("app");
  if (!root) {
    rendering = false;
    return;
  }

  let route = getRoute();

  // Redirect shorthand
  if (route === "repo") {
    navigate("/repos", true);
    rendering = false;
    return;
  }

// Default root handling
if (!route) {
  const hasDashboard = routes.find(r => r.path === "dashboard");
  const hasLogin = routes.find(r => r.path === "login");

  if (hasDashboard && hasLogin) {
    if (getToken()) {
      navigate("/dashboard", true);
    } else {
      navigate("/login", true);
    }
    rendering = false;
    return;
  }
}

  const match = matchRoute(route);

  root.innerHTML = "";

  if (!match) {
    const notFound = routes.find(r => r.path === "404");
    if (notFound) {
      notFound.handler(root, {});
    } else {
      root.innerHTML = `
        <div class="card">
          <h2>404</h2>
          <div class="dim">Route not found</div>
        </div>
      `;
    }
    rendering = false;
    return;
  }

  try {
    match.handler(root, {
      ...match.params,
      query: getQuery()
    });
  } catch (err) {
    console.error("Router error:", err);
    root.innerHTML = `
      <div class="card">
        <h2>Page Error</h2>
        <div class="dim">Something went wrong rendering this page.</div>
      </div>
    `;
  }

  rendering = false;
}

/* ============================================
   Init
============================================ */

export function initRouter() {
  window.addEventListener("popstate", render);

  document.body.addEventListener("click", (e) => {
    const link = e.target.closest("a[data-link]");
    if (!link) return;

    e.preventDefault();
    navigate(link.getAttribute("href"));
  });

  render();
}