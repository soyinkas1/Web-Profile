from app.main.config.configuration import ConfigurationManager
from app.main.component.data_cleaning import DataIngestion
from app.main.logging import logging
from app.main.exception import CustomException
import sys

STAGE_NAME = "Data Ingestion"


class DataIngestionPipeline:

    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()


if __name__ == '__main__':
    try:
        logging.info(f'>>>>>{STAGE_NAME} stage started <<<<<<')
        obj = DataIngestionPipeline()
        obj.main()
        logging.info(f'>>>>> {STAGE_NAME}stage completed <<<<<<\n\n x===========x')

    except Exception as e:
        raise CustomException(e, sys)