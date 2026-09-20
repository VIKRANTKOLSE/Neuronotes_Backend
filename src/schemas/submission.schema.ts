import {z} from "zod";

export const submissionSchema=z.object({
    userId:z.number().int().positive(),
    questionId:z.number().int().positive(),
    answer:z.number().int().positive()
})