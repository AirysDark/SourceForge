import "../components/commit-graph.js";
class SfRepo extends HTMLElement{
connectedCallback(){
this.innerHTML=`
<div class="card">
<h2>Enterprise DAG (10k commits)</h2>
<sf-commit-graph></sf-commit-graph>
</div>`;
}
}
customElements.define("sf-repo",SfRepo);
