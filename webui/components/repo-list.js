class SfRepoList extends HTMLElement {
  set data(val) { this._data = val; this.render(); }
  render() {
    if (!this._data) return;
    this.innerHTML = this._data.map(r => `
      <div class="repo-row">
        <div><strong>${r.name}</strong><br><span style="color:var(--sf-text-dim)">${r.desc}</span></div>
        <div><span class="badge">${r.visibility}</span></div>
        <div style="color:var(--sf-text-dim)">${r.updated}</div>
      </div>
    `).join('');
  }
}
customElements.define('sf-repo-list', SfRepoList);
