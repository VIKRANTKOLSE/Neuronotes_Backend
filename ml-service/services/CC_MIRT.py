from fastapi import HTTPException
from logging import critical
import logging
from copy import Error
import math
import numpy as np
from models.CC_MIRT import PredictionRequest,PredictResponse
from config.database import app
from services.users import change_theta
async def predict_probability(data:PredictionRequest):
    try:
        predProbability=0.25+0.75*(1/(1+(math.exp(-0.45))))
        
    except ValueError as ve:
        logging.error(f"Math/validation Error in CC-MIRT: {str(ve)}")
        raise HTTPException(status_code=422,detail=ve)
        
    except Exception as e:
        logging.critical(f"Fatal ML Pipeline Execution: {str(e)}")
        raise HTTPException(status_code=500,detail=e)
    return PredictResponse(
        prediction=round(predProbability),
        probability=predProbability
    )