# Import the required libraries
import os
import sys
import pandas as pd
from demo_app1.app.main.logging import logging
from box.exceptions import BoxValueError
from box import ConfigBox
import yaml
from pathlib import Path
from typing import Any
from ensure import ensure_annotations
from demo_app1.app.main.exception import CustomException
import dill

from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, GridSearchCV



def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f'yaml file: {path_to_yaml} loaded successfully')
            return ConfigBox(content)

    except BoxValueError:
        raise ValueError('yaml file is empty')
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    create list of directories

    Arg:
        path_to_directories (list): list of path of directories
    
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging\
                .info(f'created directory at: {path}')


@ensure_annotations
def save_object(file_path: str | os.PathLike, obj):
    """
    Saves the object as a pickle file on the file_path provided
    
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file_obj:
        dill.dump(obj, file_obj)


@ensure_annotations
def load_object(file_path: str | os.PathLike):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
        

@ensure_annotations    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        """
        This method fits and score the models provided while doing a gridsearch cross
        validation using the parameter grid provided
        
        input: X-train - Training data input features
             y_train - Training data label 
             X_test - Test data input features
             y_test - Test data labels
             models - ML model to experiment with
             param :dict - parameter settings to try as values.
             
        Returns: a dictionary of the a key values pair of model and score
        """ 
        def get_object(class_path):
            """
            get the class object from the string returned from YAML 
            """
            module_name, class_name = class_path.rsplit('.', 1)
            module = __import__(module_name, fromlist=[class_name])
            
            return getattr(module, class_name)()
        
        for model_name, class_path in models.items():
             models[model_name] = get_object(class_path)
                
        report = {}
     
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]
                     
            gs = GridSearchCV(model, para, cv=3, verbose=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            test_model_score = model.score(X_test, y_test)

            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise e
