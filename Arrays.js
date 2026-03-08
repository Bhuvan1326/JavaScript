// let arr=[1,2,3,4,5]
//console.log(arr)

// for(let i=0;i<arr.length;i++)
// {
//     console.log(arr[i]);
// }

// for(let num of arr)
// {
//     console.log(num);
// }


// let marks=[85,97,44,37,76,60];
// let sum=0;
// for(let i=0;i<marks.length;i++)
// {
//   sum +=marks[i];
// }
// let avg=sum/6;
// console.log("The avg of marks =",avg);



// let items=[250,645,300,900,50];
// for(let i=0;i<items.length;i++)
// {
//     let offer=items[i]/10;
//     items[i]=items[i]-offer;
// }

// console.log(items);



let company=["Bloomberg","Microsoft","Uber","Google","IBM","Netflix"];
company.shift();
console.log(company);
company.splice(1,1,"Ola");
console.log(company);
company.push("Amazon");
console.log(company);

