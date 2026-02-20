import { apiGet } from "../api.js";

class SfSearchBox extends HTMLElement{
connectedCallback(){
this.innerHTML=`<div class="card">
<input class="input" placeholder="Search…" />
<div class="results"></div>
</div>`;
this.querySelector("input").addEventListener("input",e=>this.doSearch(e.target.value));
}
async doSearch(q){
if(!q){this.querySelector(".results").innerHTML="";return;}
const r=await apiGet(`/search?q=${encodeURIComponent(q)}`);
this.querySelector(".results").innerHTML=`
<div><strong>Repos:</strong> ${r.repos.map(x=>x.name).join(", ")}</div>
<div><strong>Code:</strong> ${r.code.map(x=>x.path).join(", ")}</div>
<div><strong>Issues:</strong> ${r.issues.map(x=>x.title).join(", ")}</div>
`;
}
}
customElements.define("sf-search-box",SfSearchBox);
