class SfPrDetail extends HTMLElement{

async connectedCallback(){
const res=await fetch("webui/data/pr.json");
this.pr=await res.json();
this.activeTab="conversation";
this.render();
}

setTab(tab){
this.activeTab=tab;
this.render();
}

render(){

const approved = this.pr.reviews.filter(r=>r.state==="APPROVED").length;
const ciPassing = this.pr.ci.every(c=>c.status==="passing");
const mergeAllowed = approved >= this.pr.required_reviews && ciPassing;

this.innerHTML=`
<div class="card">
<h2>PR #${this.pr.id}: ${this.pr.title}</h2>

<div class="tabs">
<div class="tab ${this.activeTab==="conversation"?"active":""}" data-tab="conversation">Conversation</div>
<div class="tab ${this.activeTab==="files"?"active":""}" data-tab="files">Files Changed</div>
<div class="tab ${this.activeTab==="checks"?"active":""}" data-tab="checks">Checks</div>
</div>

${this.renderTabContent(approved,ciPassing)}

<button class="${mergeAllowed ? "" : "disabled"}">
${mergeAllowed ? "Merge Pull Request" : "Merge Blocked"}
</button>
</div>
`;

this.querySelectorAll(".tab").forEach(t=>{
t.onclick=()=>this.setTab(t.dataset.tab);
});
}

renderTabContent(approved,ciPassing){

if(this.activeTab==="conversation"){
return `
<div class="panel">
${this.pr.reviews.map(r=>`
<div class="timeline-item">
<strong>${r.user}</strong> — ${r.state}
</div>`).join("")}
<div><strong>Approved:</strong> ${approved}/${this.pr.required_reviews}</div>
</div>`;
}

if(this.activeTab==="files"){
return `
<div class="panel">
${this.pr.diff.map(d=>`
<div class="${d.type==="add"?"diff-add":"diff-del"}">
${d.line}
</div>`).join("")}
</div>`;
}

if(this.activeTab==="checks"){
return `
<div class="panel">
${this.pr.ci.map(c=>`
<div>${c.name}: ${c.status}</div>`).join("")}
<div><strong>All Passing:</strong> ${ciPassing}</div>
</div>`;
}

return "";
}

}

customElements.define("sf-pr-detail",SfPrDetail);
