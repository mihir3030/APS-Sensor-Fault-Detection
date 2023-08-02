import os

# defining comman constant for training pipeline
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "ApsSensor"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "sensor.csv"

TRAINING_FILE_NAME: str = "training.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"
MODEL_FILE_NAME: str = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEME_DROPS_COLS = "drop_columns"


"""
Data Ingestion constants - starts with DATA_INGESTION var name
"""
DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_STORE_DIR_NAME: str = "feature_store"
DATA_INGESTED_INGESTED_DIR: str = "ingested"
DATA_INGESTION_SPLIT_RATIO: float = 0.2
