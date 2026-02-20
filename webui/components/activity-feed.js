class SfActivityFeed extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h4>Recent Activity</h4>
        <div class="list-row"><div>Repo created</div><div>user</div><div>1h ago</div></div>
        <div class="list-row"><div>Issue opened</div><div>user</div><div>3h ago</div></div>
      </div>
    `;
  }
}
customElements.define('sf-activity-feed', SfActivityFeed);
