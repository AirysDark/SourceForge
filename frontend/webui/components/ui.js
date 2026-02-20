import {api} from "../api.js";

class SfGitCRDT extends HTMLElement{
connectedCallback(){
this.innerHTML=`<div class="card">
<h3>Git-Aware CRDT (Commit DAG)</h3>
<input class="repo" placeholder="repo">
<textarea class="commit" placeholder='{"sha":"abc","parents":[]}'></textarea>
<button class="add">Add Commit</button>
<button class="get">Get DAG</button>
<pre class="out"></pre>
</div>`;

this.q(".add").onclick=async()=>{
 const repo=this.v(".repo");
 const data=JSON.parse(this.q(".commit").value);
 const r=await api.addCommit(repo,data);
 this.msg(r);
};
this.q(".get").onclick=async()=>{
 const r=await api.getDag(this.v(".repo"));
 this.msg(r);
};
}
q(s){return this.querySelector(s);}
v(s){return this.querySelector(s).value;}
msg(o){this.q(".out").textContent=JSON.stringify(o,null,2);}
}
customElements.define("sf-git-crdt",SfGitCRDT);
