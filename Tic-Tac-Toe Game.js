let btn = document.querySelectorAll(".box");
let b = document.querySelector("#b");
let newbtn=document.querySelector("#n");
let container=document.querySelector(".msg-container");
let p=document.querySelector("#ko");
let h=document.querySelector("#h");

let player1 = true;
let count=0;
let winnerFound=false;

let winpatterns=[
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
];
function resetGame()
 {
  player1=true;
 boxesEnabled();
 count=0;
 container.classList.add("hide");
 }

 btn.forEach((box)=>{
    box.addEventListener("click",()=>{
    if(player1 === true)  {
        box.innerHTML="X";
        box.style.color="rgb(216, 175, 52)";
        player1=false;
    }else{
        box.innerHTML="O";
        box.style.color="rgb(216, 68, 233)";
        player1=true;
    }
    box.disabled=true;
    count++;
    checkWinner();
  });
 });
 let boxesDisabled=()=>
 {
    for(let box of btn){
        box.disabled=true;
    }
 }
  let boxesEnabled=()=>
 {
    for(let box of btn){
        box.disabled=false;
        box.innerHTML="";
    }
 }
let shoWinner=(winner)=>
{
    p.innerHTML=`Winner is ${winner}` ;
    container.classList.remove("hide");
    boxesDisabled();
}
 let checkWinner = ()=>{
   
   for(let pattern of winpatterns) 
    {
    let pos1=btn[pattern[0]].innerText;
    let pos2=btn[pattern[1]].innerText;
    let pos3=btn[pattern[2]].innerText;

    if(pos1 !=="" && pos2 !=="" && pos3 !=="")
    {
        if(pos1===pos2 && pos2===pos3)
        {
            console.log("Winner",pos1);
            shoWinner(pos1);
            winnerFound=true;
        }
    }
    if(count ===9 && !winnerFound)
    {
        p.innerHTML="Draw"
        container.classList.remove("hide");
    }
   }
 }

 newbtn.addEventListener("click",resetGame);
 b.addEventListener("click",resetGame);

