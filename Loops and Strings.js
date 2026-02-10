// console.log("Even numbers from 0 to 100");
// for(let i=0;i<=100;i=i+2)
// {
//     console.log(i)
// }



// console.log("Number guessing game")
// let num=25;

// let num1=prompt("Enter a number:")
// while(num != num1){
// if(num>num1)
// {
//     num1=prompt("You guessed wrong.Go for higher number");
// }
// else if(num<num1)
// {
//     num1=prompt("You guessed wrong.Go for lower number");
// }
// }
// console.log("You found the number");



// let str=`The addition of 1,107,45 is ${1+107+45}`;
// console.log(str)
// let product={
//     name:"headphone",
//     price:700
// }
// console.log(`The price of ${product.name} is ${product.price}`)
// //using Template literals easy readable the price 700 is converted into string

// console.log("The price of",product.name,"is",product.price)



let user=prompt("Enter your full name(Don't add space in between your name)");
let user_name=`@${user}${user.length}`;
console.log(user_name);