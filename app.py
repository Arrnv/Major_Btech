from fastapi import FastAPI
import numpy as np
import pandas as pd
from pydantic import BaseModel
from src.pipeline.prediction_pipeline import PredictPipeline

class CustomData(BaseModel):
    age: int
    gender: int
    height: float
    weight: float
    ap_hi: int
    ap_lo: int
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    cardio:int
    age_years: int
    bmi:float
    bp_category:str
    bp_category_encoded:str

app = FastAPI()

@app.post("/predict")
async def predict(data: CustomData):
    predict_pipeline = PredictPipeline()
    df = pd.DataFrame([data.dict()])
    preds = predict_pipeline.predict(df)
    if isinstance(preds, np.ndarray):
        preds = preds.tolist()
    elif not isinstance(preds, (list, dict, str, int, float)):
        preds = str(preds)
    return {"preds": preds[0]}