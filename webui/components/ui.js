// webui/components/ui.js

import { apiPost, apiGet } from "../api.js";

class SfGitCRDT extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>Git-Aware CRDT (Commit DAG)</h3>
        <input class="repo" placeholder="repo">
        <textarea class="commit" placeholder='{"sha":"abc","parents":[]}'></textarea>
        <button class="add">Add Commit</button>
        <button class="get">Get DAG</button>
        <pre class="out"></pre>
      </div>
    `;

    this.querySelector(".add").onclick = async () => {
      try {
        const repo = this.value(".repo");
        const data = JSON.parse(this.value(".commit"));
        const r = await apiPost(`/repos/${repo}/commit`, data);
        this.msg(r);
      } catch (e) {
        this.msg({ error: e.message });
      }
    };

    this.querySelector(".get").onclick = async () => {
      try {
        const repo = this.value(".repo");
        const r = await apiGet(`/repos/${repo}/dag`);
        this.msg(r);
      } catch (e) {
        this.msg({ error: e.message });
      }
    };
  }

  value(sel) {
    return this.querySelector(sel).value;
  }

  msg(o) {
    this.querySelector(".out").textContent =
      JSON.stringify(o, null, 2);
  }
}

customElements.define("sf-git-crdt", SfGitCRDT);