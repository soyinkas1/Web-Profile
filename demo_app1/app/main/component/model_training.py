# Import Data Analysis Libraries
import pandas as pd
import numpy as np
import os
import dill
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Import Machine Learning Classifiers models Libraries
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
import lightgbm as lgb
from xgboost import XGBClassifier


# Import evaluations modules
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import RocCurveDisplay


# Import other needed machine Learning Libraries
from sklearn.preprocessing import StandardScaler, OneHotEncoder,MinMaxScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, GridSearchCV
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.pipeline import Pipeline

# import the internal classes and methods required
from app.main.config.config_entity import DataTransformationConfig, ModelTrainerConfig
from app.main.exception import CustomException
from app.main.logging import logging
from app.utils.common import save_object, evaluate_models



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.model_trainer_config = config
        
        # self.clean_data_config = clean_data_config
        logging.info('Model Trainer Configuration loaded...')

    def initiate_model_trainer(self):

        # We will load the training, validation and test dataset as chunks

        train_reader = pd.read_csv(self.model_trainer_config.train_data_path, chunksize=1000, low_memory=False)
        val_reader = pd.read_csv(self.model_trainer_config.val_data_path, chunksize=1000, low_memory=False)
        test_reader = pd.read_csv(self.model_trainer_config.test_data_path, chunksize=1000, low_memory=False)

        # Concatenate all chunks into a single DataFrame
        train = pd.concat(train_reader)
        val = pd.concat(val_reader)
        test = pd.concat(test_reader)

        logging.info('Dataset loaded ...')

      
        # Split the data into input features and target labels
        X_train, y_train, X_val, y_val, X_test, y_test = train.iloc[:, :-1],train.iloc[:, -1], val.iloc[:, :-1], val.iloc[:, -1],test.iloc[:, :-1], test.iloc[:, -1]

        logging.info('Dataset split completed...')

        # Evaluate the model and append its score to model_report
        model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test=X_val, y_test=y_val, models=self.model_trainer_config.models, param=self.model_trainer_config.params)
        
        logging.info('Models evaluated for best one...')   
        # To get best model score from dict
        best_model_score = max(sorted(model_report.values()))
        
        # To get best model name from dict
        best_model_name = list(model_report.keys())[
                    list(model_report.values()).index(best_model_score)
                ]
        best_model = self.model_trainer_config.models[best_model_name]

        if best_model_score < 0.6:
            raise CustomException("No best model found")
            
        logging.info(f"Best found model on both training and testing dataset")

        save_object(
                    file_path=self.model_trainer_config.best_model_path,
                    obj= best_model
                )

        return print(f'Best Model: {best_model}, Score: {best_model_score}')
                        


