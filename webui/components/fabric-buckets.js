class SfFabricBuckets extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>SourceFabric Buckets</h3>
        <div class="tree-row">🧊 cold-core</div>
        <div class="tree-row">🧊 repo-archive</div>
        <div class="tree-row">🧊 nightly-snapshots</div>
      </div>
    `;
  }
}
customElements.define('sf-fabric-buckets', SfFabricBuckets);
