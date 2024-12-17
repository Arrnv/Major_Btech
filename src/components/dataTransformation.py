import sys
from dataclasses import dataclass
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        """
        This function si responsible for data trnasformation
        """
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
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),  
                ('cat', OneHotEncoder(drop='first'), categorical_features) 
            ]
        )
        return preprocessor
    def initiate_data_transformation(self,raw_data_path):
        try:
            df = pd.read_csv(raw_data_path)
            logging.info("Reading the data completed")
            
            df['age'] = df['age'] / 365.25
            df = df.rename(columns={'ap_hi': 'systolic_b_pressure'})
            df = df.rename(columns={'ap_lo': 'diastolic_b_pressure'})
            df = df.rename(columns={'gluc': 'glucose'})
            df = df.rename(columns={'alco': 'alcohol'})
            df = df.rename(columns={'active': 'physically_active'})
            df = df.rename(columns={'cardio': 'cardio_disease'})
            #data cleaning
            df = df[(df['height'] >= 100) & (df['height'] <= 200)]

            df = df[(df['weight'] >= 40) & (df['weight'] <= 200)]

            df = df[(df['systolic_b_pressure'] >= 90) & (df['systolic_b_pressure'] <= 250)]
            df = df[(df['diastolic_b_pressure'] >= 60) & (df['diastolic_b_pressure'] <= 150)]

            df = df[df['cholesterol'].isin([1, 2, 3])]
            df = df[df['glucose'].isin([1, 2, 3])]

            df = df.dropna()
            df = df[df['gender'].isin([1, 2])]
            #Creating New Features
            df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
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
            data_encoded = pd.get_dummies(df, columns=non_numeric_columns, drop_first=True)
            data_encoded.drop(columns=['height_weight_ratio', 'weight', 'cholesterol', 'pressure_ratio'], inplace=True)
            features_to_drop = [
                'gender', 'smoke', 'alcohol', 'physically_active', 
                'pressure_ratio', 'weight', 'height_weight_ratio', 'cholesterol'
            ]

            features_to_drop = [col for col in features_to_drop if col in data_encoded.columns]
            print("Features to drop:", features_to_drop)

            data_encoded_cleaned = data_encoded.drop(columns=features_to_drop)
            print(data_encoded_cleaned.info())
            X = data_encoded_cleaned.drop(columns=['id', 'cardio_disease'])
            y = data_encoded_cleaned['cardio_disease']
            
            y = y.astype(int)
            processer = self.get_data_transformer_object()
            X_transformed = processer.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=processer

            )   
            return (
                X_train, 
                X_test, 
                y_train, 
                y_test
            )
        except Exception as e:
            raise CustomException(e,sys)