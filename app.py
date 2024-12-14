# from src.logger import logging
# from src.exception import CustomException
import sys
from src.components.dataInject import DataInjection, DataInjectionConfig
from src.components.dataTransformation import DataTransformation
from src.components.dataTransformation import DataTransformationConfig

from src.components.modeltrainer import ModelTrainerConfig
from src.components.modeltrainer import ModelTrainer

if __name__=="__main__":
    obj=DataInjection()
    raw_data_path=obj.initate_data_injection()

    data_transformation=DataTransformation()
    X_train, X_test, y_train, y_test=data_transformation.Initate_data_transformation(raw_data_path)

    modeltrainer=ModelTrainer()
    print(modeltrainer.InitateModelTrainer(X_train, X_test, y_train,  y_test))