// webui/pages/repos.js

import { apiGet } from "../api.js";
import { navigate } from "../core/router.js";

export async function reposPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Repositories</h2>
      <div class="dim">Loading...</div>
    </div>
  `;

  try {

    const repos = await apiGet("/repos");

    content.innerHTML = `
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <h2>Repositories</h2>
          <button class="btn-create">+ New Repo</button>
        </div>

        <div id="repoList">
          ${
            repos.length === 0
              ? `<div class="dim">No repositories yet.</div>`
              : repos.map(r => `
                  <div class="table-row repo-item" data-id="${r.id}">
                    <div>
                      <strong>${r.name}</strong>
                      <div class="dim" style="font-size:12px;">
                        ${r.description || ""}
                      </div>
                    </div>
                    <div class="badge">${r.visibility || "private"}</div>
                  </div>
                `).join("")
          }
        </div>
      </div>
    `;

    content.querySelector(".btn-create").onclick = () => {
      navigate("/create-repo");
    };

    content.querySelectorAll(".repo-item").forEach(el => {
      el.onclick = () => {
        navigate(`/repo/${el.dataset.id}`);
      };
    });

  } catch (err) {
    console.error(err);
    content.innerHTML = `
      <div class="card">
        <h2>Repositories</h2>
        <div class="dim">Unable to load repositories.</div>
      </div>
    `;
  }
}