// webui/pages/create-pr.js

import { apiPost } from "../api.js";
import { navigate } from "../core/router.js";

export function createPrPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Create Pull Request</h2>

      <div style="display:flex;flex-direction:column;gap:8px;">
        <input id="repoId" placeholder="Repository ID" />
        <input id="title" placeholder="PR Title" />
        <textarea id="desc" placeholder="Description"></textarea>
        <button id="createPrBtn">Create PR</button>
        <div class="msg dim"></div>
      </div>
    </div>
  `;

  const msg = content.querySelector(".msg");

  content.querySelector("#createPrBtn").onclick = async () => {

    const repoId = content.querySelector("#repoId").value.trim();
    const title = content.querySelector("#title").value.trim();
    const description = content.querySelector("#desc").value.trim();

    if (!repoId || !title) {
      msg.textContent = "Repository ID and title are required.";
      return;
    }

    try {
      const pr = await apiPost(`/pr/${repoId}/create`, {
        title,
        description
      });

      msg.className = "";
      msg.textContent = "Pull Request created.";

      setTimeout(() => {
        navigate(`/repo/${repoId}`);
      }, 800);

    } catch (err) {
      console.error(err);
      msg.className = "dim";
      msg.textContent = "Failed to create PR.";
    }
  };
}