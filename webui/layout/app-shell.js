class SfApp extends HTMLElement{

async connectedCallback(){
const res=await fetch("webui/data/state.json");
this.state=await res.json();
this.connectWebSocket();
this.render();
}

connectWebSocket(){
this.ws=new WebSocket("ws://localhost:8765");
this.ws.onmessage=(event)=>{
const msg=JSON.parse(event.data);
if(msg.type==="notification"){
this.state.notifications.unshift({text:msg.text});
}
if(msg.type==="queue"){
this.state.mergeQueue.unshift(msg.item);
}
this.render();
};
}

render(){
this.innerHTML=`
<div class="topbar">
<strong>SourceForge (Live)</strong>
<span class="badge">${this.state.notifications.length}</span>
</div>

<div class="card">
<h2>Merge Queue</h2>
${this.state.mergeQueue.map(q=>`
<div class="queue-item">#${q.id} — ${q.title}</div>
`).join("")}
</div>

<div class="card">
<h2>Notifications</h2>
${this.state.notifications.map(n=>`
<div class="notification">${n.text}</div>
`).join("")}
</div>
`;
}
}

customElements.define("sf-app",SfApp);
