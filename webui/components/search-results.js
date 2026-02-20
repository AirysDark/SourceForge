class SfSearchResults extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>Search Results</h3>
        <div class="search-row"><strong>SourceForge-Core</strong><br><span style="color:var(--sf-text-dim)">Repository match</span></div>
        <div class="search-row"><strong>repo-viewer.js</strong><br><span style="color:var(--sf-text-dim)">Code match</span></div>
        <div class="search-row"><strong>Issue: Improve UI</strong><br><span style="color:var(--sf-text-dim)">Issue match</span></div>
      </div>
    `;
  }
}
customElements.define('sf-search-results', SfSearchResults);
