class SfIssueList extends HTMLElement {
  async connectedCallback() {
    const res = await fetch('webui/data/mock.json');
    const data = await res.json();
    this.innerHTML = data.issues.map(i => `
      <div class="issue-row">
        <div>${i.title}</div>
        <div><span class="badge">${i.status}</span></div>
        <div></div>
      </div>
    `).join('');
  }
}
customElements.define('sf-issue-list', SfIssueList);
