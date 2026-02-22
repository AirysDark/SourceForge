// webui/components/repos.js

import { apiGet } from "../api.js";

class SfRepos extends HTMLElement {
  connectedCallback() {
    this.load();
  }

  async load() {
    try {
      const repos = await apiGet("/repos");

      this.innerHTML = `
        <div class="card">
          <h3>Repositories</h3>
          ${
            repos.length === 0
              ? `<div class="dim">No repositories</div>`
              : repos.map(x =>
                  `<div class="repo-row">${x.name}</div>`
                ).join("")
          }
        </div>
      `;
    } catch {
      this.innerHTML = `
        <div class="card">
          Auth required
        </div>
      `;
    }
  }
}

customElements.define("sf-repos", SfRepos);