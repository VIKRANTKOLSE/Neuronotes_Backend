import { Router} from "express"
import {createSubmission} from "../controllers/submissions.controller.js"

const router=Router()

router.post("/",createSubmission)

export default router