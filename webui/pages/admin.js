class SfAdmin extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `
      <div class="card">
        <h2>Admin / Infra</h2>
        <p>Replication, metrics, and CRDT state will display here.</p>
      </div>
    `;
  }
}
customElements.define("sf-admin", SfAdmin);
