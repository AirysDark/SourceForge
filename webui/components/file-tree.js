class SfFileTree extends HTMLElement {
  set data(val) { this._data = val; this.render(); }
  render() {
    if (!this._data) return;
    this.innerHTML = this._data.map(f => `
      <div class="file-row">
        <div>${f.type === 'dir' ? '📁' : '📄'} ${f.name}</div>
        <div></div>
        <div style="color:var(--sf-text-dim)">${f.updated}</div>
      </div>
    `).join('');
  }
}
customElements.define('sf-file-tree', SfFileTree);
