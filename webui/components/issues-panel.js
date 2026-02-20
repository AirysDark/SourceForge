class SfIssuesPanel extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>Issues</h3>
        <div class="tree-row">🐛 Sidebar glitch</div>
        <div class="tree-row">✨ Add dark mode toggle</div>
        <div class="tree-row">🚀 Improve repo speed</div>
      </div>
    `;
  }
}
customElements.define('sf-issues-panel', SfIssuesPanel);
