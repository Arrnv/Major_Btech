import pandas as pd
from src.pipeline.prediction_pipeline import PredictPipeline

# Define the input data model
custom_input_data = {
  "age": 16424,  # age in days (roughly 45 years)
  "gender": 1,  # Male
  "height": 170,  # cm
  "weight": 75,  # kg
  "ap_hi": 130,  # Systolic BP
  "ap_lo": 85,  # Diastolic BP
  "cholesterol": 2,  # Cholesterol level
  "gluc": 1,  # Glucose level
  "smoke": 0,  # Does not smoke
  "alco": 1,  # Drinks alcohol
  "active": 1,  # Active
  "cardio": 0  # No cardio disease
}

# Convert the input data into a pandas DataFrame
input_df = pd.DataFrame([custom_input_data])

# Initialize the prediction pipeline
predict_pipeline = PredictPipeline()

# Use the predict method on the input data
try:
    # Make predictions
    predictions = predict_pipeline.predict(input_df)
    print(f"Predictions: {predictions}")
except Exception as e:
    print(f"Error: {str(e)}")