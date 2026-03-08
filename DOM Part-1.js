// console.log(window.document.body);
// let p=document.getElementById("para");
// console.dir(p);

// let h=document.getElementsByClassName("bhu");
//console.log(h);
// console.dir(h);

// let s=document.getElementsByTagName("p");
// console.dir(s);
// console.log(s);

// let el=document.querySelector("p");//returns the 1st p element from html
// console.dir(el);

// let el1=document.querySelectorAll("p");//returns a NodeList of all p element from html
// console.dir(el1);

// let el2=document.querySelector(".bhu");//returns the 1st class with name bhu element from html
// console.dir(el2);

// let el3=document.querySelectorAll(".bhu");//returns a NodeList of all p element from html
// console.dir(el3);

// const p01 = document.getElementById("para-01");
// console.log(p01.firstChild.nodeName);

// let div=document.querySelector("div");
// console.dir(div);

// let hi=document.getElementById("rr");
// console.dir(hi);

// let oi=document.getElementById("o");

// oi.append(" From Bhuvan Patil");
// console.dir(oi);

// let h2=document.querySelector("h2");
// h2.append(" from Bhuvan Patil")

let divs=document.querySelectorAll(".box");
let i=1;
for(div of divs)
{
    div.innerText=`This is new div: ${i}`;
    i++;
}