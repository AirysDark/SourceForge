// webui/pages/pr-list.js

import { apiGet } from "../api.js";
import { navigate } from "../core/router.js";

export async function prListPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Pull Requests</h2>
      <div id="prContainer" class="dim">Loading...</div>
    </div>
  `;

  const container = content.querySelector("#prContainer");

  try {

    // Adjust endpoint if needed
    const prs = await apiGet("/pr");

    if (!prs || prs.length === 0) {
      container.innerHTML = `<div class="dim">No pull requests found.</div>`;
      return;
    }

    container.innerHTML = prs.map(pr => `
      <div class="table-row pr-row" data-repo="${pr.repo}" data-id="${pr.id}">
        <div>
          <strong>#${pr.id}</strong> — ${pr.title || "Untitled PR"}
        </div>
        <div class="badge">${pr.status || "open"}</div>
      </div>
    `).join("");

    container.querySelectorAll(".pr-row").forEach(row => {
      row.onclick = () => {
        const repo = row.dataset.repo;
        const id = row.dataset.id;
        navigate(`/repo/${repo}?pr=${id}`);
      };
    });

  } catch (err) {
    console.error(err);
    container.innerHTML = `
      <div class="dim">
        Failed to load pull requests.
      </div>
    `;
  }
}