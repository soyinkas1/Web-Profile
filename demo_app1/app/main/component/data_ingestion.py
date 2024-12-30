import sys
import pandas as pd
from app.main.exception import CustomException
from app.main.logging import logging

import warnings

from app.main.config.config_entity import DataIngestionConfig
from app.main.config.configuration import ConfigurationManager

warnings.filterwarnings("ignore")

class DataIngestion:
    """
    Class object that defines the data ingestion stage of the project
    """
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config

    def initiate_data_ingestion(self):
        """ The method to ingest data from data sources"""
        logging.info('Started the data ingestion process...')
        
        try:
            
            dfs = pd.read_csv(self.ingestion_config.raw_data_path, chunksize=self.ingestion_config.chunk_size,
                                  low_memory=True, nrows=self.ingestion_config.n_rows)
            df = pd.concat(dfs)

            logging.info('Read the heart disease dataset as dataframe')

            df.to_csv(self.ingestion_config.loaded_data_path, index=False)

            logging.info('Saved the loaded heart disease dataset in csv format')

        
        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == '__main__':
#     config = ConfigurationManager()
#     data_ingestion_config = config.get_data_ingestion_config()
#     obj= DataIngestion(config=data_ingestion_config)
#     obj.initiate_data_ingestion()

