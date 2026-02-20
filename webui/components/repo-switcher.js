import { apiGet } from "../api.js";

class SfRepoSwitcher extends HTMLElement{
connectedCallback(){this.load();}
async load(){
const repos=await apiGet("/repos");
this.innerHTML=`<div class="card"><strong>Repos</strong>${
repos.map(r=>`<div class="tree-row" data-id="${r.id}">${r.name}</div>`).join("")
}</div>`;
this.querySelectorAll(".tree-row").forEach(r=>{
r.onclick=()=>{
location.hash=`repo:${r.dataset.id}`;
};
});
}
}
customElements.define("sf-repo-switcher",SfRepoSwitcher);
