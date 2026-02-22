// webui/pages/dashboard.js

import { apiGet } from "../api.js";

export async function dashboardPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Dashboard</h2>
      <div id="status" class="dim">Loading system status...</div>
    </div>

    <div class="card">
      <h3>Overview</h3>
      <div id="overview" class="dim">Loading data...</div>
    </div>
  `;

  const statusBox = content.querySelector("#status");
  const overviewBox = content.querySelector("#overview");

  try {

    const health = await apiGet("/health");
    statusBox.innerHTML = `
      Status: <span class="badge">${health.status}</span>
    `;

  } catch {
    statusBox.innerHTML = `<span class="dim">Health check failed</span>`;
  }

  try {

    const repos = await apiGet("/repos");

    let prCount = 0;
    try {
      const prs = await apiGet("/pr");
      prCount = prs.length;
    } catch {}

    overviewBox.innerHTML = `
      <div>Repositories: <strong>${repos.length}</strong></div>
      <div>Pull Requests: <strong>${prCount}</strong></div>
    `;

  } catch {
    overviewBox.innerHTML = `<span class="dim">Unable to load overview data</span>`;
  }
}