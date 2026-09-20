from typing import Annotated
from pydantic import BaseModel,ConfigDict,Field

class PredictionRequest(BaseModel):
    model_config=ConfigDict(extra="forbid")
    userId:Annotated[int,Field(gt=0)]
    questionId:Annotated[int,Field(gt=0)]
    answer:Annotated[int,Field(gt=0,lt=5)]

class PredictResponse(BaseModel):
    prediction:int
    probability:Annotated[float,Field(ge=0,le=1)]

