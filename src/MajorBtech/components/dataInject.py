import os 
import sys
from src.MajorBtech.exception import CustomException
from src.MajorBtech.logger import logging
import pandas as pd
from dataclasses import dataclass
from src.MajorBtech.utils import read_sql_data

@dataclass
class DataInjectionConfig:
    raw_data_path:str=os.path.join('artifact','raw.csv')
    # train_data_path:str=os.path.join('artifact','train.csv')
    # test_data_path:str=os.path.join('artifact','test.csv')
    

class DataInjection:
    def __init__(self):
        self.injection_config = DataInjectionConfig
    def initate_data_injection(self):
        try:
            df = read_sql_data()
            logging.info("reading from mysql database")
            os.makedirs(os.path.dirname(self.injection_config.raw_data_path),exist_ok=True)
            df.to_csv(self.injection_config.raw_data_path,index = False, header=True)
            # train_set, test_set = train_test_split(df, test_size=0.2, random_state=11)
            # train_set.to_csv(self.injection_config.train_data_path,index = False, header=True)
            # test_set.to_csv(self.injection_config.test_data_path,index = False, header=True)
            logging.info("Data Injection Complete")
            return (
                self.injection_config.raw_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)