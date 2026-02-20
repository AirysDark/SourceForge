class SfDashboard extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<div class="card"><h2>Dashboard</h2></div>`;
  }
}
customElements.define("sf-dashboard", SfDashboard);
