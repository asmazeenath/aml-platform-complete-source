const API=import.meta.env.VITE_API_URL || "http://localhost:8000";
export async function request(path:string,init?:RequestInit){
 const res=await fetch(`${API}${path}`,{...init,headers:{"Content-Type":"application/json",...(init?.headers||{})}});
 if(!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
 return res.json();
}
