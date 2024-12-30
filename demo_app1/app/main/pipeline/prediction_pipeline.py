import sys
import pandas as pd
from pyparsing import cached_property
from app.main.exception import CustomException
from app.utils.common import load_object
from app.main.config.config_entity import PredictionPipelineConfig
from app.main.logging import logging

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
            preprocessor_path=self.prediction_config.preprocessor_path
            print("Before Loading model and preprosessor")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading model and preprosessor")

            
            data_scaled=preprocessor.transform(features)
            data_scaled.shape
            preds=model.predict(data_scaled)
            return preds
             # Load the preprocessor and fit it with features
            print(features.shape)
            
        
        except Exception as e:
            raise CustomException(e,sys)



class CustomData:
    def __init__(  self, 
            age: int,
            sex:  int,
            cp: int,
            trestbpscp: int,
            chol: int,
            fbs: int,
            restecg: int,
            thalach: int,
            exang: int,
            oldpeak: float,
            slope: int,
            ca: int,
            thal: int):

        self.age=age
        self.sex=sex
        self.cp=cp
        self.trestbpscp=trestbpscp
        self.chol=chol
        self.fbs=fbs
        self.restecg=restecg
        self.thalach=thalach
        self.exang=exang
        self.oldpeak=oldpeak
        self.slope=slope
        self.ca=ca
        self.thal=thal
        
        

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "age": [self.age],
                "sex": [self.sex],
                "cp": [self.cp],
                "trestbpscp": [self.trestbpscp],
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