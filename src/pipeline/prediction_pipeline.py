import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import os


class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,features):
        """
        Initialize the prediction pipeline with the saved model and preprocessor paths.
        """
        try:
            model_path=os.path.join("models","model.pkl")
            preprocessor_path=os.path.join('artifacts','proprocessor.pkl')
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            x = self.preprocess_input_data(features)
            xt = preprocessor.transform(x)
            preds=model.predict(xt)
            print("After Loading")
            return preds
            
            
        except Exception as e:
            raise CustomException(f"Error initializing PredictPipeline: {e}", sys)
    
    def preprocess_input_data(self, df):
        try:
            # print(df)
            df['age'] = df['age'] / 365.25

            df = df.rename(columns={'ap_hi': 'systolic_b_pressure'})
            df = df.rename(columns={'ap_lo': 'diastolic_b_pressure'})
            df = df.rename(columns={'gluc': 'glucose'})
            df = df.rename(columns={'alco': 'alcohol'})
            df = df.rename(columns={'active': 'physically_active'})
            df = df.rename(columns={'cardio': 'cardio_disease'})
            print("weight Problem")
            print(df.info())
            print("did got it")
            df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
            categories = ['normal', 'prehypertension', 'hypertension']
            df['blood_pressure_category'] = pd.cut(
                df['systolic_b_pressure'], bins=[0, 120, 140, float('inf')], labels=categories)
            bins = [30, 45, 60, 80]
            labels = ['young', 'middle_aged', 'elderly']
            df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
            df['smoke_and_alcohol'] = ((df['smoke'] == 1) & (df['alcohol'] == 1)).astype(int)
            df['pressure_ratio'] = df['systolic_b_pressure'] / df['diastolic_b_pressure']
            df['cholesterol_bmi_interaction'] = df['cholesterol'] * df['bmi']
            df['height_weight_ratio'] = df['height'] / df['weight']
            df['active_with_disease'] = ((df['physically_active'] == 1) & (df['cardio_disease'] == 1)).astype(int)
            
            non_numeric_columns = df.select_dtypes(exclude=['number']).columns
            # print("Non-numeric columns:", non_numeric_columns)

            data_encoded = pd.get_dummies(df, columns=non_numeric_columns, drop_first=True)
            features_to_drop = [
                'gender', 'smoke', 'alcohol', 'physically_active', 
                'pressure_ratio', 'weight', 'height_weight_ratio', 'cholesterol', 'cardio_disease'
            ]

            features_to_drop = [col for col in features_to_drop if col in data_encoded.columns]
            # print("Features to drop:", features_to_drop)

            data_encoded_cleaned = data_encoded.drop(columns=features_to_drop)
            # print(data_encoded_cleaned.info())
            return data_encoded_cleaned
            # if isinstance(raw_data, dict):
            #     raw_data = pd.DataFrame([raw_data])
            # elif isinstance(raw_data, pd.Series):
            #     raw_data = pd.DataFrame([raw_data.to_dict()])
            
            # raw_data['age'] = raw_data['age'] / 365.25
            # raw_data = raw_data.rename(columns={
            #     'ap_hi': 'systolic_b_pressure',
            #     'ap_lo': 'diastolic_b_pressure',
            #     'gluc': 'glucose',
            #     'alco': 'alcohol',
            #     'active': 'physically_active',
            #     'cardio': 'cardio_disease'
            # })

            # # Basic cleaning (skip filtering ranges for single prediction if unsure)
            # raw_data['bmi'] = raw_data['weight'] / (raw_data['height'] / 100) ** 2
            # categories = ['normal', 'prehypertension', 'hypertension']
            # raw_data['blood_pressure_category'] = pd.cut(
            #     raw_data['systolic_b_pressure'], bins=[0, 120, 140, float('inf')], labels=categories
            # )
            # bins = [30, 45, 60, 80]
            # labels = ['young', 'middle_aged', 'elderly']
            # raw_data['age_group'] = pd.cut(raw_data['age'], bins=bins, labels=labels, right=False)
            # raw_data['smoke_and_alcohol'] = ((raw_data['smoke'] == 1) & (raw_data['alcohol'] == 1)).astype(int)
            # raw_data['cholesterol_bmi_interaction'] = raw_data['cholesterol'] * raw_data['bmi']
            # raw_data['active_with_disease'] = (
            #     (raw_data['physically_active'] == 1) & (raw_data['cardio_disease'] == 1)
            # ).astype(int)

            # processed_data = self.preprocessor.transform(raw_data)
            # logging.info("Data transformation for single input completed.")
            
            # return processed_data
        except Exception as e:
            raise CustomException(f"Error in preprocessing single input: {e}", sys)
        

