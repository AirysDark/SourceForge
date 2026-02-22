// webui/components/repo-switcher.js

import { apiGet } from "../api.js";
import { navigate } from "../core/router.js";

class SfRepoSwitcher extends HTMLElement {
  connectedCallback() {
    this.load();
  }

  async load() {
    try {
      const repos = await apiGet("/repos");

      this.innerHTML = `
        <div class="card">
          <strong>Repos</strong>
          ${repos.map(r => `
            <div class="tree-row" data-id="${r.id}">
              ${r.name}
            </div>
          `).join("")}
        </div>
      `;

      this.querySelectorAll(".tree-row").forEach(row => {
        row.onclick = () => {
          const id = row.dataset.id;

          // Navigate using clean URL routing
          navigate(`repo?id=${id}`);
        };
      });

    } catch (e) {
      this.innerHTML = `
        <div class="card">
          Failed to load repositories
        </div>
      `;
    }
  }
}

customElements.define("sf-repo-switcher", SfRepoSwitcher);