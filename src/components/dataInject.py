import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass
from src.utils import read_sql_data




@dataclass
class DataInjectionConfig:
    raw_data_path:str=os.path.join('artifact','raw.csv')
    train_data_path:str=os.path.join('artifact','train.csv')
    test_data_path:str=os.path.join('artifact','test.csv')
    

class DataInjection:
    def __init__(self):
        self.injection_config = DataInjectionConfig
    def initate_data_injection(self):
        try:
            df = read_sql_data()
            logging.info("reading from mysql database")
            os.makedirs(os.path.dirname(self.injection_config.raw_data_path),exist_ok=True)
            df.to_csv(self.injection_config.raw_data_path,index = False, header=True)
            logging.info("Data Injection Complete")
            return (
                self.injection_config.raw_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
# if __name__=="__main__":
#     obj=DataInjection()
#     raw_data_path=obj.initate_data_injection()

#     data_transformation=DataTransformation()
#     X_train, X_test, y_train, y_test=data_transformation.Initate_data_transformation(raw_data_path)

#     modeltrainer=ModelTrainer()
#     print(modeltrainer.initiate_model_trainer(X_train, X_test, y_train,  y_test))