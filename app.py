from src.MajorBtech.logger import logging
from src.MajorBtech.exception import CustomException
import sys
from src.MajorBtech.components.dataInject import DataInjection, DataInjectionConfig


if __name__=="__main__":
    logging.info("The execution has started")
    
    try:
        Datainjection=DataInjection()
        Datainjection.initate_data_injection()
        
    except Exception as e:
        raise CustomException(e,sys)