import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

from dataclasses import dataclass
@dataclass
class PredictionPipeline:
    def __init__(self):
        pass
    def predict(self, df):
        try:
            df['age'] = df['age'] / 365.25
            # df.age
            df = df.rename(columns={'ap_hi': 'systolic_b_pressure'})
            df = df.rename(columns={'ap_lo': 'diastolic_b_pressure'})
            df = df.rename(columns={'gluc': 'glucose'})
            df = df.rename(columns={'alco': 'alcohol'})
            df = df.rename(columns={'active': 'physically_active'})
            df = df.rename(columns={'cardio': 'cardio_disease'})
            
            df = df[(df['height'] >= 100) & (df['height'] <= 200)]
            df = df[(df['weight'] >= 40) & (df['weight'] <= 200)]
            df = df[(df['systolic_b_pressure'] >= 90) & (df['systolic_b_pressure'] <= 250)]
            df = df[(df['diastolic_b_pressure'] >= 60) & (df['diastolic_b_pressure'] <= 150)]
            df = df[df['cholesterol'].isin([1, 2, 3])]
            df = df[df['glucose'].isin([1, 2, 3])]
            df = df.dropna()
            df = df[df['gender'].isin([1, 2])]
            df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

            # conditions = [
            #     (df['systolic_b_pressure'] < 120) & (df['diastolic_b_pressure'] < 80),
            #     ((df['systolic_b_pressure'] >= 120) & (df['systolic_b_pressure'] < 140)) |
            #     ((df['diastolic_b_pressure'] >= 80) & (df['diastolic_b_pressure'] < 90)),
            #     (df['systolic_b_pressure'] >= 140) | (df['diastolic_b_pressure'] >= 90)
            # ]
            categories = ['normal', 'prehypertension', 'hypertension']
            df['blood_pressure_category'] = pd.cut(
                df['systolic_b_pressure'], bins=[0, 120, 140, float('inf')], labels=categories
            )
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
            
            numeric_cols = data_encoded.select_dtypes(include=['float64', 'int64']).columns
            scaler = StandardScaler()
            data_encoded[numeric_cols] = scaler.fit_transform(data_encoded[numeric_cols])
            features_to_drop = [
                'gender', 'smoke', 'alcohol', 'physically_active', 
                'pressure_ratio', 'weight', 'height_weight_ratio', 'cholesterol'
            ]
            features_to_drop = [col for col in features_to_drop if col in data_encoded.columns]
            data_encoded_cleaned = data_encoded.drop(columns=features_to_drop)
            

            X = data_encoded_cleaned.drop(columns=['id', 'cardio_disease'])
            

            numeric_features = [
                'age', 'height', 'systolic_b_pressure', 'diastolic_b_pressure', 'glucose', 
                'bmi', 'cholesterol_bmi_interaction', 'active_with_disease'
            ]

            categorical_features = [
                'blood_pressure_category_prehypertension', 
                'blood_pressure_category_hypertension', 
                'age_group_middle_aged', 
                'age_group_elderly'
            ]

            numeric_features = [col for col in numeric_features if col in X.columns]
            categorical_features = [col for col in categorical_features if col in X.columns]

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), numeric_features),  
                    ('cat', OneHotEncoder(drop='first'), categorical_features) 
                ]
            )
            
            pass
        except Exception as e:
            raise CustomException(e,sys)
class CustomInput:
    def __init__(self,
                 age: float,
                 gender: int,
                 height: int,
                 weight: int,
                 ap_hi: int,
                 ap_lo: int,
                 cholesterol: int,
                 gluc: int,
                 smoke: int,
                 alco: int,
                 active: int,
                 cardio: int,
                 age_years: int,
                 bmi: float,
                 bp_category: str,
                 bp_category_encoded: str
                 ):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.ap_hi = ap_hi  
        self.ap_lo = ap_lo  
        self.cholesterol = cholesterol
        self.gluc = gluc  
        self.smoke = smoke
        self.alco = alco
        self.active = active
        self.cardio = cardio
        self.age_years = age_years
        self.bmi = bmi
        self.bp_category = bp_category
        self.bp_category_encoded = bp_category_encoded
        
    def GetDataAsDataframe(self):
        try:
            predict_data={
                "age": self.age,
                "gender": self.gender,
                "height": self.height,
                "weight": self.weight,
                "ap_hi": self.ap_hi,
                "ap_lo": self.ap_lo,
                "cholesterol": self.cholesterol,
                "gluc": self.gluc,
                "smoke": self.smoke,
                "alco": self.alco,
                "active": self.active,
                "cardio": self.cardio,
                "age_years": self.age_years,
                "bmi": self.bmi,
                "bp_category": self.bp_category,
                "bp_category_encoded": self.bp_category_encoded
            }
            
            return pd.DataFrame(predict_data,index=[0])
        except Exception as e:
            raise CustomException(e,sys)