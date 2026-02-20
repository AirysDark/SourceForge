import { apiGet } from "../api.js";

class SfCommitsPanel extends HTMLElement{
connectedCallback(){this.repoId="repo_1";this.load();}
async load(){
const list=await apiGet(`/repos/${this.repoId}/commits`);
this.innerHTML=`<div class="card"><h3>Commits</h3>${
list.map(c=>`<div class="tree-row" data-sha="${c.sha}">${c.sha.slice(0,7)} — ${c.message}</div>`).join("")
}</div>`;
this.querySelectorAll(".tree-row").forEach(r=>r.onclick=()=>this.openDiff(r.dataset.sha));
}
async openDiff(sha){
const d=await apiGet(`/repos/${this.repoId}/commit/${sha}/diff`);
document.querySelector("sf-diff-viewer")?.setPatch(d.files?.[0]?.patch||"");
}
}
customElements.define("sf-commits-panel",SfCommitsPanel);
