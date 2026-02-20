class SfVirtualRepos extends HTMLElement {
  connectedCallback() {
    let rows = "";
    for (let i = 1; i <= 50; i++) {
      rows += `<div class="virtual-row">repo-${i}</div>`;
    }
    this.innerHTML = `<div class="card"><h3>Repositories</h3><div class="virtual-list">${rows}</div></div>`;
  }
}
customElements.define('sf-virtual-repos', SfVirtualRepos);
