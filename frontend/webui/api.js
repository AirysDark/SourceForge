export const API="http://localhost:8000/api/v1";

export const api={
 addCommit:(repo,data)=>fetch(`${API}/repo/${repo}/commit`,{
   method:"POST",headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)}).then(r=>r.json()),
 merge:(repo,data)=>fetch(`${API}/repo/${repo}/merge`,{
   method:"POST",headers:{'Content-Type':'application/json'},
   body:JSON.stringify(data)}).then(r=>r.json()),
 getDag:(repo)=>fetch(`${API}/repo/${repo}/dag`).then(r=>r.json())
};
