// webui/pages/activity.js

import { apiGet } from "../api.js";

export async function activityPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Activity Feed</h2>
      <div id="activityContainer" class="dim">Loading activity...</div>
    </div>
  `;

  const container = content.querySelector("#activityContainer");

  try {
    const data = await apiGet("/activity");

    if (!data || data.length === 0) {
      container.innerHTML = `<div class="dim">No recent activity.</div>`;
      return;
    }

    container.innerHTML = data.map(e => `
      <div class="table-row">
        <div>
          <div>${e.message || "Activity event"}</div>
          ${e.timestamp ? `
            <div class="dim" style="font-size:12px;">
              ${new Date(e.timestamp).toLocaleString()}
            </div>
          ` : ""}
        </div>
      </div>
    `).join("");

  } catch (err) {
    console.error(err);
    container.innerHTML = `<div class="dim">Unable to load activity.</div>`;
  }
}