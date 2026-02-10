// let arrowSum=(a,b)=>{
//     return a+b;
// }

// let arrowMul=(a,b)=>
// {
//     return a*b;
// }


// let name1=prompt("Enter name:")
// function vowel()
// {
//     let count=0;
//     name1=name1.toLowerCase();
//     for(let i=0;i<name1.length;i++)
//     {
//     if(name1[i]=='a'|| name1[i]=='e'|| name1[i]=='i'|| name1[i]=='o'|| name1[i]=='u')
//     {
//     count++;
//     }  
//     } 
//     console.log(count);
// };
// vowel();


// let arr=['bhuvan','bhu','good'];
// arr.forEach((val,i,arr)=>
// {
//     console.log(i,val,arr);
// });
// //High order function are function which take other functions as a parameter or return other functions

//Array methods 
//1.forEach loop
// let arr=[1,2,3,4]
// arr.forEach((val,i,arr)=>{
//     console.log(val**2);
// });


//2.map
//similar to forEach but creates a new array and the original array is untounched
// let arr=[1,2,3,4,5,6]
// let arr1=arr.map((val)=>
// {
//     return val;
// });
// console.log(arr1);

//3.filter
//creates a new array and filter out the unwanted filter out values
// let arr=[1,2,3,4,5,6]
// let arr1=arr.filter((val)=>
// {
//     return val %2 ===0 ;
// });
// console.log(arr1);

//4.reduce
//Forms opertions on array where multiple inputs have 1 single output like sum,avg of n no.
// let arr=[23,45,67,76,21]
// let arr1=arr.reduce((prev,curr)=>
// {
//     return prev+curr;
// })
// console.log(arr1);



//Q1
//Take a random array of marks of students.Filter out marks more than 90
// let marks=[80,91,98,56,34,93]
// let sub=marks.filter((val)=>
// {
//     return val>90;
// });
// console.log(sub);



//Q2
//Take a num n as input from user.Create an array of nums from 1 to n
//Ex:If user enters 4 array must be of [1,2,3,4]
//Use the reduce method to calculate sum of all nums
//Use the reduce method to calculate product of all nums

let n=prompt("Enter a number:");
let arr=[];
for(let i=1;i<=n;i++)
{
    arr[i-1]=i;
}
console.log(arr);
let arr1=arr.reduce((prev,curr)=>
{
    return prev+curr;
});
console.log("Sum= ",arr1);
let arr2=arr.reduce((prev,curr)=>
{
    return prev*curr;
});
console.log("Product= ",arr2);

