class SfPRPanel extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>Pull Requests</h3>
        <div class="commit-row">🔀 #42 — Add repo virtualization</div>
        <div class="commit-row">🔀 #41 — Fix sidebar collapse</div>
        <div class="commit-row">🔀 #40 — Improve search ranking</div>
      </div>
    `;
  }
}
customElements.define('sf-pr-panel', SfPRPanel);
