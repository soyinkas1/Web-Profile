from app.main.config.configuration import ConfigurationManager
from app.main.component.model_training import ModelTrainer
from app.main.logging import logging
from app.main.exception import CustomException
import sys
# from src.entity.config_entity import ModelTrainerConfig

STAGE_NAME = "Model Trainer"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.initiate_model_trainer()


if __name__ == '__main__':
    try:
        logging.info(f'>>>>>stage {STAGE_NAME} started <<<<<<')
        obj = ModelTrainerPipeline()
        obj.main()
        logging.info(f'>>>>>stage {STAGE_NAME} completed <<<<<<\n\n x===========x')

    except Exception as e:
        raise CustomException(e, sys)
