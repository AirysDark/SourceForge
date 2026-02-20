class SfCommitGraph extends HTMLElement{

connectedCallback(){
this.innerHTML=`
<div style="position:relative">
<canvas width="1200" height="600"></canvas>
<canvas class="minimap" width="200" height="120"></canvas>
</div>`;

this.canvas=this.querySelector("canvas");
this.ctx=this.canvas.getContext("2d");
this.minimap=this.querySelector(".minimap");
this.mctx=this.minimap.getContext("2d");

this.scale=1;
this.offsetY=0;
this.visibleStart=0;
this.visibleCount=200;

this.fetchData();
}

async fetchData(){
const res=await fetch("webui/data/dag.json");
this.commits=await res.json();
this.layout();
this.draw();
}

layout(){
const laneMap={};
let lane=0;
this.nodes=this.commits.map((c,i)=>{
if(!laneMap[c.sha]) laneMap[c.sha]=lane;
return{
...c,
lane:laneMap[c.sha],
x:100+laneMap[c.sha]*80,
y:50+i*40
};
});
}

draw(){
this.ctx.setTransform(1,0,0,1,0,0);
this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
this.ctx.translate(0,this.offsetY);
this.ctx.scale(this.scale,this.scale);

const start=this.visibleStart;
const end=Math.min(start+this.visibleCount,this.nodes.length);

for(let i=start;i<end;i++){
const n=this.nodes[i];
n.parents.forEach(p=>{
const parent=this.nodes.find(x=>x.sha===p);
if(parent){
this.ctx.strokeStyle="#FF6A00";
this.ctx.beginPath();
this.ctx.moveTo(n.x,n.y);
this.ctx.lineTo(parent.x,parent.y);
this.ctx.stroke();
}
});
this.ctx.beginPath();
this.ctx.arc(n.x,n.y,5,0,Math.PI*2);
this.ctx.fillStyle="#FF6A00";
this.ctx.fill();
}

this.drawMinimap();
}

drawMinimap(){
this.mctx.clearRect(0,0,this.minimap.width,this.minimap.height);
const total=this.nodes.length;
const scaleY=this.minimap.height/total;
this.mctx.fillStyle="#FF6A00";
this.nodes.forEach((n,i)=>{
this.mctx.fillRect(10,i*scaleY,5,1);
});
}

}
customElements.define("sf-commit-graph",SfCommitGraph);
