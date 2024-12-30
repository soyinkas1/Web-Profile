import sys
import pandas as pd
from app.main.exception import CustomException
from app.main.logging import logging

import warnings

from app.main.config.config_entity import DataCleaningConfig, DataTransformationConfig
from app.main.config.configuration import ConfigurationManager

from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

class DataTransformation:
    """
    Class object that carries out the data transformation steps and splits the data ready for model training. 
    """
    def __init__(self, config: DataTransformationConfig):
        self.transformation_config = config

    def initiate_data_transformation(self):
        """ The method to transform the cleaned data as feature matrix and target vector then into training and test dataset after all other necessary transformations"""
        
        logging.info('Started the data transformation process...')
        
        try:
            # read the cleaned heart disease dataset as chunks
            dfs = pd.read_csv(self.transformation_config.clean_data_path, chunksize=self.transformation_config.chunk_size,
                                  low_memory=True)
            
            # Create a DataFrame from uploaded chunks
            df = pd.concat(dfs)

            logging.info('Read the cleaned heart disease dataset as dataframe')

            '''
            Any future transformation steps required will be added here
            
            ''' 

            # # Split the data into X and y
            # X= df.drop('target',axis=1)
            # y = df.target
            
            logging.info('Dataset split into features matrix and target vector')
            
            # Split the data into train and test sets
            train,val,test = train_test_split(df,train_size=0.6, test_size=0.2)
            print('Shape of train:', train.shape,'Shape of val:',val.shape,'Shape of test:',test.shape)
            
            logging.info('Datasets split into training and test datasets')

            # Save the train and test datasets
            
            train.to_csv(self.transformation_config.train_data_path, index=False)
            test.to_csv(self.transformation_config.test_data_path, index=False)
            val.to_csv(self.transformation_config.val_data_path, index=False)
            # y_test.to_csv(self.transformation_config.y_test_data_path, index=False)

            logging.info('Training and test datasets saved for next stage- modelling')
            
                    
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == '__main__':
    config = ConfigurationManager()
    data_transformation_config = config.get_data_transformation_config()
    obj= DataTransformation(config=data_transformation_config)
    obj.initiate_data_transformation()