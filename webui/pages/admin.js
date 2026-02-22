// webui/pages/admin.js

import { apiGet } from "../api.js";

export async function adminPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>System Status</h2>
      <div id="health" class="dim">Checking health...</div>
    </div>

    <div class="card">
      <h2>Metrics</h2>
      <div id="metrics" class="dim">Loading metrics...</div>
    </div>
  `;

  const healthBox = content.querySelector("#health");
  const metricsBox = content.querySelector("#metrics");

  /* ===============================
     Health Check
  ================================= */

  try {
    const health = await apiGet("/health");
    healthBox.innerHTML = `
      <div>Status: <span class="badge">${health.status}</span></div>
    `;
  } catch (err) {
    console.error(err);
    healthBox.innerHTML = `<div class="dim">Health check failed</div>`;
  }

  /* ===============================
     Metrics
  ================================= */

  try {
    const metrics = await apiGet("/metrics");

    if (typeof metrics === "string") {
      metricsBox.innerHTML = `
        <pre style="white-space:pre-wrap;font-size:12px;">
${metrics}
        </pre>
      `;
    } else {
      metricsBox.innerHTML = `
        <pre>${JSON.stringify(metrics, null, 2)}</pre>
      `;
    }

  } catch (err) {
    console.error(err);
    metricsBox.innerHTML = `<div class="dim">Metrics unavailable</div>`;
  }
}