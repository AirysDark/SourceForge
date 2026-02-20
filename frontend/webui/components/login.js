import { login } from "../api.js";

class SfLogin extends HTMLElement{
connectedCallback(){
this.innerHTML=`<div class="card">
<h3>Login</h3>
<input class="u" placeholder="username">
<input class="p" placeholder="password" type="password">
<button class="log">Login</button>
<div class="msg"></div></div>`;
this.querySelector(".log").onclick=()=>this.doLog();
}
async doLog(){await login(this.q(".u"),this.q(".p"));this.msg("Logged in");}
q(s){return this.querySelector(s).value;}
msg(t){this.querySelector(".msg").textContent=t;}
}
customElements.define("sf-login",SfLogin);
