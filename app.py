from src.logger import logging
from src.exception import CustomException
import sys
import random

# from src.components.dataInject import DataInjection
# from src.components.dataTransformation import DataTransformation

# from src.components.modeltrainer import ModelTrainer

# if __name__=="__main__":
#     obj=DataInjection()
#     raw_data_path=obj.initate_data_injection()

#     data_transformation=DataTransformation()
#     X_train, X_test, y_train, y_test=data_transformation.Initate_data_transformation(raw_data_path)

#     modeltrainer=ModelTrainer()
#     print(modeltrainer.InitateModelTrainer(X_train, X_test, y_train,  y_test))



from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
from typing import List
from src.pipeline.prediction_pipeline import CustomInput,PredictionPipeline




pipeline = PredictionPipeline()

class InputData(BaseModel):
    age: float
    gender: int
    height: int
    weight: int
    ap_hi: int
    ap_lo: int
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    cardio: int
    age_years: int
    bmi: float
    bp_category: str
    bp_category_encoded: str


app = FastAPI()


@app.post("/predict")
async def predict_data(input_data: InputData):
    """
    Endpoint to receive input data, process it, and return the prediction.
    """
    try:
        input_data.cardio = random.randint(0, 1)
        # Convert InputData into CustomInput
        custom_input = CustomInput(
            age=input_data.age,
            gender=input_data.gender,
            height=input_data.height,
            weight=input_data.weight,
            ap_hi=input_data.ap_hi,
            ap_lo=input_data.ap_lo,
            cholesterol=input_data.cholesterol,
            gluc=input_data.gluc,
            smoke=input_data.smoke,
            alco=input_data.alco,
            active=input_data.active,
            cardio=input_data.cardio,
            age_years=input_data.age_years,
            bmi=input_data.bmi,
            bp_category=input_data.bp_category,
            bp_category_encoded=input_data.bp_category_encoded
        )


        input_df = custom_input.GetDataAsDataframe()
        # print(input_df)
        # Perform prediction
        prediction = pipeline.predict(input_df)

        return {"prediction": prediction.tolist(), "message": "Prediction successful"}
    except Exception as e:
        raise CustomException(e,sys)

# @app.get("/submissions")
# async def get_submissions():
#     return {"submissions": submissions}