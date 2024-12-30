
from demo_app1.app.utils.common import read_yaml, create_directories
from demo_app1.app.main.config.config_entity import DataIngestionConfig, DataCleaningConfig, DataTransformationConfig,ModelTrainerConfig, PredictionPipelineConfig, WebFormConfig
import os
from demo_app1.app.main.constants import *

basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigurationManager:

    def __init__(self,config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath) 
        self.params = read_yaml(params_filepath)
        
        create_directories([self.config.artifacts_root])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(   
        root_dir=config.root_dir,
        n_rows=config.n_rows,
        raw_data_path=config.raw_data_path,
        loaded_data_path=config.loaded_data_path,
        chunk_size=config.chunk_size

        )

        return data_ingestion_config
    
    def get_data_cleaning_config(self) -> DataCleaningConfig:
        config = self.config.data_cleaning

        create_directories([config.root_dir])

        data_cleaning_config = DataCleaningConfig(   
        root_dir=config.root_dir,
        loaded_data_path=config.loaded_data_path,
        clean_data_path=config.clean_data_path,
        chunk_size=config.chunk_size

        )

        return data_cleaning_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
        root_dir=config.root_dir, 
        clean_data_path=config.clean_data_path,
        transformed_data_path=config.transformed_data_path,
        chunk_size=config.chunk_size, 
        train_data_path=config.train_data_path,
        test_data_path=config.test_data_path,
        val_data_path=config.val_data_path,
        
        )

        return data_transformation_config

    def get_data_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.param_grid

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
                root_dir=config.root_dir, 
                best_model_path=config.best_model_path,
                train_data_path=config.train_data_path,
                test_data_path=config.test_data_path,
                val_data_path=config.val_data_path,
                models=config.models,
                params=params.params
            
            )

        return model_trainer_config
            

    def get_prediction_pipeline_config(self) -> PredictionPipelineConfig:
        config = self.config.prediction_pipeline

        prediction_pipeline_config = PredictionPipelineConfig(
                age=config.age,
                sex=config.sex,
                cp=config.cp,
                trestbpscp=config.trestbpscp,
                chol=config.chol,
                fbs=config.fbs,
                restecg=config.restecg,
                thalach=config.thalach,
                exang=config.exang,
                oldpeak=config.oldpeak,
                slope=config.slope,
                ca=config.ca,
                thal=config.thal,
                model_path=config.model_path,
                preprocessor_path=config.preprocessor_path
            )

        return prediction_pipeline_config
        
    def get_webform_config(self) -> WebFormConfig:
        config = self.config.webform

        webform_config = WebFormConfig(
                    sex=config.sex,
                    fbs=config.fbs,
                    restecg=config.restecg  
                    
            )

        return webform_config
        