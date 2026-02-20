class SfPrList extends HTMLElement{

async connectedCallback(){
const res=await fetch("webui/data/prs.json");
this.prs=await res.json();
this.render();
}

render(){
this.innerHTML=`
<div class="card">
<h2>Pull Requests</h2>
${this.prs.map(pr=>`
<div class="table-row">
<div>
<strong>#${pr.id}</strong> ${pr.title}<br>
<small>by ${pr.author}</small>
</div>
<div>
<span class="badge ${pr.status}">${pr.status}</span>
<button data-id="${pr.id}">View</button>
</div>
</div>`).join("")}
</div>
<sf-pr-detail></sf-pr-detail>
`;

this.querySelectorAll("button").forEach(btn=>{
btn.onclick=()=>{
const id=parseInt(btn.dataset.id);
const event=new CustomEvent("open-pr",{detail:id});
this.dispatchEvent(event);
};
});

this.addEventListener("open-pr",e=>{
const detail=this.querySelector("sf-pr-detail");
detail.load(e.detail);
});
}
}

customElements.define("sf-pr-list",SfPrList);
