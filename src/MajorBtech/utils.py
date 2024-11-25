import os 
import sys
from src.MajorBtech.exception import CustomException
from src.MajorBtech.logger import logging
import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()
host= os.getenv("host")
user=os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")


def read_sql_data():
    logging.info("reading sql database")
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        logging.info(f"Connection established with {mydb}")
        df = pd.read_sql_query('select * from cardio_data_processed',mydb)
        print(df.head())
        return df
        
    except Exception as e:
        raise CustomException(e, sys)
    