import type {Request,Response} from "express"
import { submissionSchema } from "../schemas/submission.schema.js";
import {Engine} from "../services/mlService.js"
import {processSubmission} from "../services/submissions.service.js"


export const createSubmission=async (req:Request,res:Response)=>{
    const parseResult = submissionSchema.safeParse(req.body);
    if(!parseResult.success){
        return res.status(400).json({
            error:"Invalid request payload",
            details:parseResult.error.issues
        })
    }
    try {
        const submission = await processSubmission(parseResult.data)
        const prediction = await Engine(parseResult.data)
        return res.status(201).json({
            message:"Submission accepted",
            submission,
            prediction
        })
    } catch (error) {
        console.error("Failed to process submission:",error);
        
        return res.status(500).json({
            message:"Failed to process submission"
        })
    }

}