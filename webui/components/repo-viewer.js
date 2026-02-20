import { apiGet } from "../api.js";

class SfRepoViewer extends HTMLElement{
connectedCallback(){
this.repoId="repo_1";
this.path="/";
window.addEventListener("hashchange",()=>this.handleRoute());
this.handleRoute();
}
handleRoute(){
const h=location.hash||"";
if(h.startsWith("#repo:")){
this.repoId=h.split(":")[1];
}
this.render();
this.loadTree("/");
}
render(){
this.innerHTML=`<div style="display:grid;grid-template-columns:260px 1fr;gap:12px;">
<div class="card"><div class="tree">Loading…</div></div>
<div class="card"><h4 class="title">Select file</h4><div class="code-view"></div></div>
</div>`;
}
async loadTree(p){
this.path=p;
const d=await apiGet(`/repos/${this.repoId}/tree?path=${encodeURIComponent(p)}`);
const c=this.querySelector(".tree");
c.innerHTML=d.entries.map(e=>`<div class="tree-row" data-t="${e.type}" data-n="${e.name}">${e.type==="dir"?"📁":"📄"} ${e.name}</div>`).join("");
c.querySelectorAll(".tree-row").forEach(r=>r.onclick=()=>{
const t=r.dataset.t,n=r.dataset.n,full=this.join(this.path,n);
if(t==="dir") this.loadTree(full); else this.openFile(full);
});
}
async openFile(p){
const d=await apiGet(`/repos/${this.repoId}/blob?path=${encodeURIComponent(p)}`);
this.querySelector(".title").textContent=p;
this.querySelector(".code-view").textContent=d.content;
}
join(b,n){return b==="/" ? `/${n}` : `${b}/${n}`;}
}
customElements.define("sf-repo-viewer",SfRepoViewer);
