import sys
import pandas as pd
from app.main.exception import CustomException
from app.main.logging import logging

import warnings

from app.main.config.config_entity import DataCleaningConfig
from app.main.config.configuration import ConfigurationManager

warnings.filterwarnings("ignore")

class DataCleaning:
    """
    Class object that defines the data cleaning stage of the project
    """
    def __init__(self, config: DataCleaningConfig):
        self.cleaning_config = config

    def initiate_data_cleaning(self):
        """ The method to clean the raw data downloaded from data sources"""
        
        logging.info('Started the data cleaning process...')
        
        try:
            # read the loaded heart disease dataset as chunks
            dfs = pd.read_csv(self.cleaning_config.loaded_data_path, chunksize=self.cleaning_config.chunk_size,
                                  low_memory=True)
            
            # Create a DataFrame from uploaded chunks
            df = pd.concat(dfs)

            logging.info('Read the loaded heart disease dataset as dataframe')

            '''
            Any future cleaning steps required will be added here
            
            '''           
            # Save the clean dataset in the data cleaning directory
            df.to_csv(self.cleaning_config.clean_data_path, index=False)

            logging.info('Saved the cleaned heart disease dataset in csv format')

        
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == '__main__':
    config = ConfigurationManager()
    data_cleaning_config = config.get_data_cleaning_config()
    obj= DataCleaning(config=data_cleaning_config)
    obj.initiate_data_cleaning()