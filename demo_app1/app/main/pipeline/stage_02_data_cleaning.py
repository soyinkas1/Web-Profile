from app.main.config.configuration import ConfigurationManager
from app.main.component.data_cleaning import DataCleaning
from app.main.logging import logging
from app.main.exception import CustomException
import sys
from app.main.config.config_entity import DataCleaningConfig

STAGE_NAME = "Data Cleaning"

class DataCleaningPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_cleaning_config = config.get_data_cleaning_config()
        data_cleaning = DataCleaning(config=data_cleaning_config)
        data_cleaning.initiate_data_cleaning()
        
if __name__ == '__main__':
    try:
        logging.info(f'>>>>> {STAGE_NAME} stage started <<<<<<')
        obj = DataCleaningPipeline()
        obj.main()
        logging.info(f'>>>>> {STAGE_NAME} stage completed <<<<<<\n\n x===========x')

    except Exception as e:
        raise CustomException(e, sys)