class SfCommitList extends HTMLElement {
  async connectedCallback() {
    const res = await fetch('webui/data/mock.json');
    const data = await res.json();
    this.innerHTML = data.commits.map(c => `
      <div class="commit-row">
        <div>${c.msg}</div>
        <div>${c.author}</div>
        <div>${c.time}</div>
      </div>
    `).join('');
  }
}
customElements.define('sf-commit-list', SfCommitList);
