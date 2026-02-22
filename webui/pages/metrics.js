// webui/pages/metrics.js

import { apiGet } from "../api.js";

export async function metricsPage(content) {

  content.innerHTML = `
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <h2>System Metrics</h2>
        <button id="refreshMetrics">Refresh</button>
      </div>
      <div id="metricsBox" class="dim">Loading metrics...</div>
    </div>
  `;

  const box = content.querySelector("#metricsBox");

  async function loadMetrics() {
    box.className = "dim";
    box.textContent = "Loading metrics...";

    try {
      const data = await apiGet("/metrics");

      box.className = "";
      if (typeof data === "string") {
        box.innerHTML = `
          <pre style="white-space:pre-wrap;font-size:12px;">
${data}
          </pre>
        `;
      } else {
        box.innerHTML = `
          <pre style="font-size:12px;">
${JSON.stringify(data, null, 2)}
          </pre>
        `;
      }

    } catch (err) {
      console.error(err);
      box.className = "dim";
      box.textContent = "Unable to load metrics.";
    }
  }

  content.querySelector("#refreshMetrics").onclick = loadMetrics;

  await loadMetrics();
}