export const API_BASE="http://localhost:8000/api/v1";
let AUTH_TOKEN=null;

export function setToken(t){AUTH_TOKEN=t;}
export function getToken(){return AUTH_TOKEN;}

export async function apiGet(path){
  const r=await fetch(API_BASE+path,{
    headers: AUTH_TOKEN?{Authorization:`Bearer ${AUTH_TOKEN}`}:{}
  });
  if(!r.ok) throw new Error("API "+r.status);
  return r.json();
}
