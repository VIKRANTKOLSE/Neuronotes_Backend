from services.users import update_theta
from fastapi import FastAPI,HTTPException
import logging
from config.database import app
from models.CC_MIRT import PredictionRequest,PredictResponse
from services.calculations import probability,adaptive_selection
from services.users import get_theta
async def predict_probability(app:FastAPI,data:PredictionRequest):
    try:
        theta = await get_theta(app, data.userId)
        
        # 1. Compute probability for the question just answered (using current theta)
        current_prob = await probability(app, data.questionId, data.userId, theta)
        
        # 2. Update the user's theta based on their answer
        updated_theta = await update_theta(app, data.userId, data.questionId, data.answer, current_prob, theta)
        
        # 3. Select the next best question using the NEW theta
        j = await adaptive_selection(app, data.userId, updated_theta)
        
        # 4. Compute probability for the next question
        predProbability = await probability(app, j, data.userId, updated_theta)
    except ValueError as ve:
        logging.error(f"Math/validation Error in CC-MIRT: {str(ve)}")
        raise HTTPException(status_code=422,detail=ve)
        
    except Exception as e:
        logging.critical(f"Fatal ML Pipeline Execution: {str(e)}")
        raise HTTPException(status_code=500,detail=e)
    return PredictResponse(
        prediction=round(predProbability),
        probability=predProbability,
        next_best_qid=j
    )