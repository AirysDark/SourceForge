class SfRepoTree extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <div class="tree-row">📁 src</div>
        <div class="tree-row">📁 webui</div>
        <div class="tree-row">📄 index.html</div>
        <div class="tree-row">📄 README.md</div>
      </div>
    `;
  }
}
customElements.define('sf-repo-tree', SfRepoTree);
