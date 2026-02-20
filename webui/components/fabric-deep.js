class SfFabricDeep extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>SourceFabric Explorer</h3>
        <div class="tree-row">🧊 cold-core / repo-001.tar</div>
        <div class="tree-row">🧊 cold-core / repo-002.tar</div>
        <div class="tree-row">🧊 nightly / snapshot.img</div>
      </div>
    `;
  }
}
customElements.define('sf-fabric-deep', SfFabricDeep);
