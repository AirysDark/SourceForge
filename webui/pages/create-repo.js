// webui/pages/create-repo.js

import { apiPost } from "../api.js";
import { navigate } from "../core/router.js";

export function createRepoPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Create Repository</h2>

      <div style="display:flex;flex-direction:column;gap:8px;">
        <input id="repoName" placeholder="Repository name" />
        <textarea id="repoDesc" placeholder="Description"></textarea>

        <select id="repoVisibility">
          <option value="private">Private</option>
          <option value="public">Public</option>
        </select>

        <button id="createRepoBtn">Create Repository</button>
        <div class="msg dim"></div>
      </div>
    </div>
  `;

  const msg = content.querySelector(".msg");

  content.querySelector("#createRepoBtn").onclick = async () => {

    const name = content.querySelector("#repoName").value.trim();
    const description = content.querySelector("#repoDesc").value.trim();
    const visibility = content.querySelector("#repoVisibility").value;

    if (!name) {
      msg.textContent = "Repository name required.";
      return;
    }

    try {

      const repo = await apiPost("/repos", {
        name,
        description,
        visibility
      });

      msg.className = "";
      msg.textContent = "Repository created.";

      setTimeout(() => {
        navigate(`/repo/${repo.id}`);
      }, 700);

    } catch (err) {
      console.error(err);
      msg.className = "dim";
      msg.textContent = "Failed to create repository.";
    }
  };
}