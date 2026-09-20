from fastapi import APIRouter
from services.CC_MIRT import predict_probability
from models.CC_MIRT import PredictionRequest,PredictResponse
router=APIRouter()

@router.post("/predict",response_model=PredictResponse)
def prediction(data:PredictionRequest)->PredictResponse:
    result= predict_probability(data)
    return result

