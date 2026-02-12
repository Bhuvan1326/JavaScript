let b=document.createElement("button");
b.innerHTML="submit";
document.body.append(b);

let p=document.createElement("p")
p.innerHTML="This is a p tag before button";
b.before(p);


let h1=document.createElement("h1");
h1.innerHTML="Good Morning";
b.after(h1);