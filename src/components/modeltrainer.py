from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import os
import sys
from src.utils import save_object
from sklearn.metrics import precision_score

@dataclass
class ModelTrainerConfig:
    trained_model_path = os.path.join("models","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.Model_Trainer_Config = ModelTrainerConfig()

    def InitateModelTrainer(self, X_train, X_test, y_train,  y_test):
        try:
            logging.info("Model training have started")
            hgb_model = HistGradientBoostingClassifier(random_state=42)
            svc_model = SVC(probability=True, random_state=42)  
            sgd_model = SGDClassifier(loss='log_loss', random_state=42)  

            ensemble_model = VotingClassifier(estimators=[
                ('hgb', hgb_model),
                ('svc', svc_model),
                ('sgd', sgd_model)
            ], voting='soft')
            logging.info("Creating model")
            ensemble_model.fit(X_train, y_train)
            save_object(
               file_path=self.Model_Trainer_Config.trained_model_path,
               obj=ensemble_model
            )
            y_test_pred = ensemble_model.predict(X_test)


            test_model_score = precision_score(y_test, y_test_pred)
            return test_model_score
            
        except Exception as e:
            raise CustomException(e, sys)

