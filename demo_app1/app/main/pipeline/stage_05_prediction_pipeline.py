import sys
import pandas as pd
from demo_app1.app.main.exception import CustomException
from demo_app1.app.utils.common import load_object
from demo_app1.app.main.config.configuration import ConfigurationManager
from demo_app1.app.main.config.config_entity import PredictionPipelineConfig
from demo_app1.app.main.logging import logging
from demo_app1.app.db_models import HeartPredictions
from demo_app1.app.extensions import db





class PredictPipeline:
    def __init__(self, config: PredictionPipelineConfig):    
        """
        configures the attributes of each instance of the class
        Arg: 
            Config: configuration of the attribute (configBox)
        """
        self.prediction_config = config

        logging.info('Prediction Configuration loaded...')
        

    def predict(self,features):
        """
        Carries out prediction on the features provided
        Arg: 
            Features: Features from web app on which prediction is done (DataFrame)
        """
  
        try:
            model_path=self.prediction_config.model_path
            # preprocessor_path=self.prediction_config.preprocessor_obj_path
            print("Before Loading model")
            model=load_object(file_path=model_path)
            # preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading model")

            
            # data_scaled=preprocessor.transform(features)
            # data_scaled.shape
            preds=model.predict(features)
            return preds        
        
        except Exception as e:
            raise CustomException(e,sys)



class CustomData:
    def __init__(  self, 
        email:int,
        age: int,
        sex:  int,
        cp: int,
        trestbps: int,
        chol: int,
        fbs: int,
        restecg: int,
        thalach: int,
        exang: int,
        oldpeak: float,
        slope: int,
        ca: int,
        thal: int,
        target:int
        ):

        self.email=email
        self.age=age
        self.sex=sex
        self.cp=cp
        self.trestbps=trestbps
        self.chol=chol
        self.fbs=fbs
        self.restecg=restecg
        self.thalach=thalach
        self.exang=exang
        self.oldpeak=oldpeak
        self.slope=slope
        self.ca=ca
        self.thal=thal
        self.target=target
               

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "age": [self.age],
                "sex": [self.sex],
                "cp": [self.cp],
                "trestbps": [self.trestbps],
                "chol": [self.chol],
                "fbs": [self.fbs],
                "restecg": [self.restecg],
                "thalach": [self.thalach],
                "exang": [self.exang],
                "oldpeak": [self.oldpeak],
                "slope": [self.slope],
                "ca": [self.ca],
                "thal": [self.thal],
                
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_for_database(self):
        try:
            custom_database_input_dict = {
                "email":[self.email],
                "age": [self.age],
                "sex": [self.sex],
                "cp": [self.cp],
                "trestbps": [self.trestbps],
                "chol": [self.chol],
                "fbs": [self.fbs],
                "restecg": [self.restecg],
                "thalach": [self.thalach],
                "exang": [self.exang],
                "oldpeak": [self.oldpeak],
                "slope": [self.slope],
                "ca": [self.ca],
                "thal": [self.thal],
                "target": [self.target],
                
            }

            return pd.DataFrame(custom_database_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
    
    def add_to_database(self, df):
        try:
            # Convert DataFrame to list of dictionaries
            data_dicts = df.to_dict(orient='records')

            # Bulk insert using SQLAlchemy
            db.session.bulk_insert_mappings(HeartPredictions, data_dicts)
            db.session.commit()
        except Exception as e:
            raise CustomException(e, sys)
            db.session.rollback()