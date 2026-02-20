class SfFabricBrowser extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>SourceFabric Objects</h3>
        <div class="tree-row">📦 cold-storage-001</div>
        <div class="tree-row">📦 project-archive</div>
        <div class="tree-row">📦 snapshot-2026</div>
      </div>
    `;
  }
}
customElements.define('sf-fabric-browser', SfFabricBrowser);
