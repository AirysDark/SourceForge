import { apiGet } from "../api.js";

class SfRepoViewer extends HTMLElement {

  connectedCallback() {
    this.repoId = this.getAttribute("repo-id") || "1";
    this.path = "/";
    this.render();
    this.loadTree("/");
  }

  render() {
    this.innerHTML = `
      <div style="display:grid;grid-template-columns:260px 1fr;gap:12px;">
        <div class="card">
          <div class="tree">Loading...</div>
        </div>
        <div class="card">
          <h4 class="title">Select file</h4>
          <div class="code-view"></div>
        </div>
      </div>
    `;
  }

  async loadTree(path) {
    try {
      this.path = path;

      const d = await apiGet(
        `/repos/${this.repoId}/tree?path=${encodeURIComponent(path)}`
      );

      const container = this.querySelector(".tree");

      container.innerHTML = d.entries.map(e => `
        <div class="tree-row" data-type="${e.type}" data-name="${e.name}">
          ${e.type === "dir" ? "📁" : "📄"} ${e.name}
        </div>
      `).join("");

      container.querySelectorAll(".tree-row").forEach(row => {
        row.onclick = () => {
          const name = row.dataset.name;
          const type = row.dataset.type;
          const full = this.path === "/" ? `/${name}` : `${this.path}/${name}`;

          if (type === "dir") {
            this.loadTree(full);
          } else {
            this.openFile(full);
          }
        };
      });

    } catch (err) {
      console.error("Tree load error:", err);
      this.querySelector(".tree").innerHTML =
        `<div class="dim">Unable to load tree</div>`;
    }
  }

  async openFile(path) {
    try {
      const d = await apiGet(
        `/repos/${this.repoId}/blob?path=${encodeURIComponent(path)}`
      );

      this.querySelector(".title").textContent = path;
      this.querySelector(".code-view").textContent = d.content;

    } catch (err) {
      console.error("Blob load error:", err);
      this.querySelector(".code-view").textContent =
        "Unable to load file";
    }
  }
}

customElements.define("sf-repo-viewer", SfRepoViewer);