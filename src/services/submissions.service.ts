import userPool from "../config/db.js"
type submissionData={
    userId:number,
    questionId:number,
    answer:number
}

export async function processSubmission(data:submissionData){
    const {userId,questionId,answer}=data;
    try{
        const result = await userPool.query(
            "INSERT INTO submissions (userid,questid,answer) VALUES ($1,$2,$3) RETURNING subid,created_at;",
            [userId,questionId,answer]
        );
        console.log("Submission recorded succesfully");
        return result.rows[0]
    }catch(error){
        console.error("Database query failed:",error);
        throw new Error("DATABASE_WRITE_FAILED",{cause:error})
    }
}