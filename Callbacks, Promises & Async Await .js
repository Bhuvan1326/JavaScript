//Asynchronous
//It allows js to execute other code while waiting for long operations to complete instead of blocking the program
console.log("1");
console.log("2");

setTimeout(()=>{
    console.log("hello");
},4000);

console.log("3");
console.log("4");



//Callback
function sum(a,b){
    console.log(a+b);
}

function callback(a,b,c)
{
    c(a,b);
}

callback(5,10,(a,b)=>{
    callback(a,b,sum)
})


function bhu(dataInt,nextdata){
    setTimeout(()=>{
        console.log("Hello",dataInt);
        if(nextdata){
            nextdata();
        }
    },2000);
}

//Callback Hell
//Nested callback is called callback hell as it is very difficult  to understand
bhu(1,()=>{
    bhu(2,()=>{
        bhu(3);
    })
})

//Promise
let p=new Promise((resolve,reject)=>{
        // resolve(123);
    reject("execption");
});


//let var_name=bhu1(value);
//Is the request send to the API to fetch value and result in sucess
//In most real-world developers work with functions that already return Promises
let bhu1=((data1,data2)=>{
    return new Promise((resolve,reject)=>{
    setTimeout(()=>{
    console.log("Data",data1);
    resolve("sucess");
    if(data2)
    {
        data2();
    }
   },5000);
  })
})

let getPrmoise=()=>{
    return new Promise((resolve,reject)=>{
        console.log("Good morning");
        //resolve("success");
        reject("unexpected error");
    })
    }

    let promise=getPrmoise();
    promise.then((res)=>{
        console.log("Promise fulfilled",res);
    })
    
    //It is excuted when i promise fails
    promise.catch((err)=>{
        console.log("Promise has been rejected",err);
    })


let bhu3=()=>{
    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
            console.log("Bhu3");
            resolve("Good job fetching bhu3");
        },3000);
    })
}

let bhu4=()=>{
    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
        console.log("Bhu4");
        resolve("Good job fetching f4")
        },2000);
    })
}

//Promise Chaning
//When multiple .then() methods are connected so that each runs after the previous promise is resolved.
// They are better to understand than Callback Hell
console.log("Fetching Bhu3");
bhu3().then((res)=>
{
    console.log("Result,",res)
    console.log("Fetching Bhu4");
    bhu4().then((res)=>{
        console.log("Result,",res)
    })
})


let hi=()=>{
    return new Promise((resolve,reject)=>{
        resolve(5);
    })
}

hi().then((res)=>{
    console.log(res)
    return res*2;
}).then((res)=>{
    console.log(res)
    return res*2;
}).then((res)=>{
    console.log(res)
    return res*2;
})


let bhu=()=>{
    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
            console.log("Result");
            resolve("Successful");
        },2000)
    });
};

// Async-Await 
// It is used as a alternative for callback hell and promise chaining and it is easier to understand

//IIFE:Immediately Invoked Function Expression 
//Automatically executes doesn't need to call the function
(async function (){
    let resolve=await hi();
    console.log(resolve);

    console.log(resolve*2);

    console.log("Fetching bhu3");
    let p=await bhu3();
    console.log(p);

    console.log("Fetching bhu4");
    let p1=await bhu4();
    console.log(p1);


})();
