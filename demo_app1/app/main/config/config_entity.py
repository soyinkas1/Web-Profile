from dataclasses import dataclass # type: ignore
import os
from pathlib import Path

from numpy.core.arrayprint import str_format # type: ignore


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    n_rows: int
    raw_data_path: Path
    loaded_data_path: Path
    chunk_size: int

@dataclass(frozen=True)
class DataCleaningConfig:
    root_dir: Path
    loaded_data_path: Path
    clean_data_path: Path
    chunk_size: int

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    clean_data_path: Path
    transformed_data_path: Path
    chunk_size: int
    train_data_path: Path
    test_data_path: Path
    val_data_path: Path
    # y_test_data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    best_model_path: Path
    train_data_path: Path
    test_data_path: Path
    val_data_path: Path
    models : dict
    params: dict

@dataclass(frozen=True)
class PredictionPipelineConfig:
    age: int
    sex:  int
    cp: int
    trestbpscp: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    model_path: Path
    preprocessor_path: Path


@dataclass(frozen=True)
class WebFormConfig:
    sex: int
    fbs: int
    restecg: int






@dataclass(frozen=True)
class WebFormConfig:
    email: str
    age: int
    sex: int
    cp: int | float
    trestbps: int | float
    chol: int | float
    fbs: int | float
    restecg: int | float
    thalach: int | float
    exang : int | float
    oldpeak: int | float
    ca: int | float
    thal: int | float 



