let b1=document.querySelector("button");

b1.onclick=(i)=> {
    console.log("Hi! Bhuvan");
    console.log(i);
    console.log(i.type);
    console.log(i.target);// returns the html tag of the event
    console.log(i.clientX, i.clientY);//defines the  position of the event
}

let b2=document.querySelector("div");
b2.addEventListener("click",()=>{
    console.log("The div was clicked");
})

const kfhr=() => {
    console.log("The button was clicked bhuvan");
}

b1.addEventListener("click",kfhr);
   
let b=document.querySelector("#b");//to identify button using id
let mode="dark";
b.addEventListener("click",()=>{
    if(mode == "dark")
    {
        mode = "light";
        document.body.style.backgroundColor="rgb(212, 239, 201)";
    }
    else{
        mode = "dark";
        document.body.style.backgroundColor=" rgb(32, 106, 2)";
    }
    console.log(mode);

})

b1.removeEventListener("click",kfhr);

