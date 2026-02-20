class SfRepoCode extends HTMLElement {
  async connectedCallback() {
    const res = await fetch('webui/data/sample.json');
    const data = await res.json();
    this.tree = data.tree;
    this.path = [];
    this.render();
  }

  getNode() {
    let node = this.tree;
    for (const p of this.path) {
      node = node.children.find(c => c.name === p);
    }
    return node;
  }

  openDir(name) {
    this.path.push(name);
    this.render();
  }

  goUp(index) {
    this.path = this.path.slice(0, index);
    this.render();
  }

  renderBreadcrumb() {
    const parts = ['root', ...this.path];
    return parts.map((p,i) =>
      `<span onclick="this.getRootNode().host.goUp(${i})" style="cursor:pointer">${p}</span>`
    ).join(' / ');
  }

  render() {
    const node = this.getNode();
    const rows = (node.children || []).map(c => `
      <div class="file-row" onclick="${c.type==='dir' ? `this.getRootNode().host.openDir('${c.name}')` : ''}">
        <div>${c.type==='dir'?'📁':'📄'} ${c.name}</div>
        <div style="color:var(--sf-text-dim)">—</div>
        <div style="color:var(--sf-text-dim)">${c.updated || ''}</div>
      </div>
    `).join('');

    this.innerHTML = `
      <div class="breadcrumb">${this.renderBreadcrumb()}</div>
      <div class="card">${rows}</div>
    `;
  }
}
customElements.define('sf-repo-code', SfRepoCode);
