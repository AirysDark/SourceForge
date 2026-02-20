class SfDiffViewer extends HTMLElement{
connectedCallback(){
this.innerHTML=`<div class="card"><h3>Side-by-Side Diff</h3>
<div class="diff-grid">
<pre class="code-view left">Select commit</pre>
<pre class="code-view right"></pre>
</div></div>`;
}
setPatch(patch){
const left=[],right=[];
patch.split("\n").forEach(l=>{
if(l.startsWith("+")){left.push("");right.push(`<span class="diff-add">${l}</span>`);}
else if(l.startsWith("-")){left.push(`<span class="diff-del">${l}</span>`);right.push("");}
else{left.push(l);right.push(l);}
});
this.querySelector(".left").innerHTML=left.join("\n");
this.querySelector(".right").innerHTML=right.join("\n");
}
}
customElements.define("sf-diff-viewer",SfDiffViewer);
