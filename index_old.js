async function callPythonFunction(a,b){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/add',
            {
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({a:a,b:b})
            }
        )
        const data = await response.json();
        console.log('Sum:',data.sum);
    } catch (error){
        console.log('Error',error)
    }
}

async function callPythonFunctionMult(a,b){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/mult',
            {
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({a:a,b:b})
            }
        )
        const data = await response.json();
        console.log('mult:',data.mult);

    } catch (error){
        console.log('Error',error)
    }
}
callPythonFunction(16,5);
callPythonFunctionMult(1,10);