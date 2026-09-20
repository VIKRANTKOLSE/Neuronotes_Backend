import submissionRouter from "./routes/submission.js";
import express from "express"

const PORT = 3000;
const app=express();

app.use(express.json());

app.use("/submissions",submissionRouter)

app.listen(PORT,()=>{
    console.log(`app running at http://localhost:${PORT}`);    
});