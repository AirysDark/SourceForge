// webui/pages/repo.js

import { apiGet } from "../api.js";

export async function repoPage(content, repoId) {

  content.innerHTML = `
    <div class="card">
      <h2>Loading repository...</h2>
    </div>
  `;

  try {

    const repo = await apiGet(`/repos/${repoId}`);

    content.innerHTML = `
      <div class="card">
        <h2>${repo.name}</h2>
        <div class="dim">${repo.description || "No description provided."}</div>
        <div style="margin-top:10px;">
          <span class="badge">ID: ${repo.id}</span>
          ${repo.default_branch ? `<span class="badge">${repo.default_branch}</span>` : ""}
        </div>
      </div>

      <sf-repo-viewer repo-id="${repoId}"></sf-repo-viewer>
    `;

  } catch (err) {
    console.error(err);
    content.innerHTML = `
      <div class="card">
        <h2>Repository Not Found</h2>
      </div>
    `;
  }
}