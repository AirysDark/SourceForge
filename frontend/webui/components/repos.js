import { apiGet, simulatePush } from "../api.js";

class SfRepos extends HTMLElement{
connectedCallback(){this.load();}
async load(){
try{
const r=await apiGet("/repos");
this.innerHTML=`<div class="card"><h3>Repos</h3>${
r.map(x=>`<div data-id="${x.id}" class="repo">${x.name}</div>`).join("")
}
<button class="push">Simulate Push</button>
<div class="msg"></div>
</div>`;

this.querySelector(".push").onclick=async()=>{
 const id=this.querySelector(".repo")?.dataset.id;
 if(!id) return;
 try{
   const res=await simulatePush(id);
   this.msg(res.message);
 }catch{
   this.msg("Write denied");
 }
};
}catch{
this.innerHTML=`<div class="card">Auth required</div>`;
}
}
msg(t){this.querySelector(".msg").textContent=t;}
}
customElements.define("sf-repos",SfRepos);
