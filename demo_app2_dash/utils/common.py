# Import the required libraries
# import re
# import os
# import pandas as pd
# import itertools
# import numpy as np
# from src.logger import logging
# # from box.exceptions import BoxValueError
# from box import ConfigBox
# import yaml
# import json
# import joblib
# from pathlib import Path
# from src.exception import CustomException
# import sys
# import dill
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics

# def read_yaml(path_to_yaml: Path) -> ConfigBox:
#     try:
#         with open(path_to_yaml) as yaml_file:
#             content = yaml.safe_load(yaml_file)
#             logging.info(f'yaml file: {path_to_yaml} loaded successfully')
#             return ConfigBox(content)

#     except BoxValueError:
#         raise ValueError('yaml file is empty')
#     except Exception as e:
#         raise e

# def save_json(path: Path, data: dict):
#     """
#     save json data

#     Args:
#     path (Path): path to json file
#     data (dict): data to be saved in json file
#     """
#     with open(path, 'w') as f:
#         json.dump(data, f, indent=4)

#     logging.info(f'json file saved at: {path}')



# def load_json(path: Path):
#     """

#     :param
#         path (Path): path to json file

#     :return:
#         ConfigBox: data as class attributes instead of dict
#     """
#     with open(path) as f:
#         content = json.load(f)

#     logging.info(f'json file loaded successfully from: {path}')
#     return content


# def save_bin(data, path: Path):
#     """
#         save binary file

#     :param
#         data (Any): data to be saved as binary
#         path (Path: path to binary file
#     :return:
#     """
#     joblib.dump(value=data, filename=path)
#     logging.info(f'binary file saved at: {path}')


# def load_bin(path: Path):
#     """
#         load binary data
#     :param
#     path (Path): path to binary file

#     :return:
#         Any: object stored in the file
#     """
#     data = joblib.load(path)
#     logging.info(f'binary file loaded from: {path}')
#     return  data

# def save_object(file_path: str , obj):
#     """
#     Saves the object as a pickle file on the file_path provided
    
#     """
#     dir_path = os.path.dirname(file_path)
#     os.makedirs(dir_path, exist_ok=True)
#     with open(file_path, 'wb') as file_obj:
#         dill.dump(obj, file_obj)


# def load_object(file_path: str ):
#     try:
#         with open(file_path, "rb") as file_obj:
#             return dill.load(file_obj)

#     except Exception as e:
#         raise CustomException(e, sys)
        
   
# def evaluate_fbp_model(train, test, cutoff, horizon, param):
#     try:
#         """
#         This method fits and score the time series models provided while doing a gridsearch cross
#         validation using the parameter grid provided
        
#         input: train - Training time series data 
#                test - Test time series data
#                models - Time series ML model to experiment with
#                param :dict - parameter settings to try as values.
             
#         Returns: a dictionary of the a key values pair of model and score
#         """ 
#         param_box = read_yaml(param)
#         param_grid = param_box.param_grid

#         # Generate all combinations of parameters
#         all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
#         rmses = []  # Store the RMSEs for each params here

#         # Use cross validation to evaluate all parameters
#         for params in all_params:
#             m = Prophet(**params).fit(train)  # Fit model with given params
#             df_cv = cross_validation(m, period=cutoff, horizon='30 days', parallel="processes")
#             df_p = performance_metrics(df_cv, rolling_window=1)
#             rmses.append(df_p['rmse'].values[0])

#         # Find the best parameters
#         tuning_results = pd.DataFrame(all_params)
#         tuning_results['rmse'] = rmses
#         return tuning_results
#     except Exception as e:
#         raise e
    

def prep_train_data_prophet(df, train_size=1):
    # lets rename the DF as required in `fbprophet`
    df_fbp = df.copy()
    df_fbp.reset_index(inplace=True)
    df_fbp.rename(columns={'value':'y', 'date': 'ds'}, inplace=True)
    df_fbp = df_fbp[['ds', 'y']]
    df_fbp.sort_values('ds',inplace=True)
    train_size = int(len(df_fbp) * train_size)

    train_df = df_fbp.iloc[:train_size]
    test_df = df_fbp.iloc[train_size:]

    
    return train_df , test_df

