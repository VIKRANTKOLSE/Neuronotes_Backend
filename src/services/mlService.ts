
type submissionPrediction={
    userId:number,
    questionId:number;
    answer:number
}

type PredictResult={
    prediction:number;
    probability:number;
}

export async function Engine(submission:submissionPrediction):Promise<PredictResult>{
    const response=await fetch("http://127.0.0.1:8000/predict",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
        },
        body:JSON.stringify(submission)
    }) 
    if(!response.ok){
        throw new Error(`ML service returned ${response}`)
    }
    return response.json() as Promise<PredictResult>
}