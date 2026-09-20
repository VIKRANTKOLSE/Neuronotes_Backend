from fastapi import APIRouter
from services.CC_MIRT import predict_probability
from models.CC_MIRT import PredictionRequest,PredictResponse
from config.database import app
router=APIRouter()

@router.post("/predict",response_model=PredictResponse)
async def prediction(data:PredictionRequest)->PredictResponse:
    result= await predict_probability(app,data)
    return result
