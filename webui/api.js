// webui/api.js

export const API_BASE = "/api";

const TOKEN_KEY = "sf_token";
let AUTH_TOKEN = localStorage.getItem(TOKEN_KEY) || null;

/* ===============================
   Token Management
================================ */

export function setToken(token) {
  AUTH_TOKEN = token;

  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function getToken() {
  return AUTH_TOKEN;
}

export function clearToken() {
  AUTH_TOKEN = null;
  localStorage.removeItem(TOKEN_KEY);
}

/* ===============================
   Core Request
================================ */

async function request(method, path, body = null) {
  const headers = {};

  if (body) {
    headers["Content-Type"] = "application/json";
  }

  if (AUTH_TOKEN) {
    headers["Authorization"] = `Bearer ${AUTH_TOKEN}`;
  }

  let response;

  try {
    response = await fetch(API_BASE + path, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });
  } catch (err) {
    throw new Error("Network error: Unable to reach backend");
  }

  const contentType = response.headers.get("content-type") || "";

  // Handle unauthorized globally
  if (response.status === 401) {
    clearToken();
    throw new Error("Unauthorized");
  }

  // Read body safely
  let rawText = "";
  try {
    rawText = await response.text();
  } catch {
    throw new Error("Failed to read response");
  }

  // Detect accidental HTML response
  if (rawText.startsWith("<!DOCTYPE") || rawText.startsWith("<html")) {
    throw new Error("Backend routing error (HTML returned)");
  }

  // Handle error status
  if (!response.ok) {
    try {
      const json = JSON.parse(rawText);
      throw new Error(json.detail || `API ${response.status}`);
    } catch {
      throw new Error(`API ${response.status}: ${rawText}`);
    }
  }

  // Return JSON if applicable
  if (contentType.includes("application/json")) {
    try {
      return JSON.parse(rawText);
    } catch {
      throw new Error("Invalid JSON response");
    }
  }

  return rawText;
}

/* ===============================
   API Methods
================================ */

export function apiGet(path) {
  return request("GET", path);
}

export function apiPost(path, data) {
  return request("POST", path, data);
}

export function apiPut(path, data) {
  return request("PUT", path, data);
}

export function apiDelete(path) {
  return request("DELETE", path);
}