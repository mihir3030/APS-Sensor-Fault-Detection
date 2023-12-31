import os

SAVED_MODEL_DIR_NAME = os.path.join("saved_models")
# defining comman constant for training pipeline
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "ApsSensor"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "sensor.csv"

TRAINING_FILE_NAME: str = "training.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"
MODEL_FILE_NAME: str = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("configs", "schema.yaml")
SCHEME_DROPS_COLS = "drop_columns"


"""
Data Ingestion constants - starts with DATA_INGESTION var name
"""
DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_STORE_DIR_NAME: str = "feature_store"
DATA_INGESTED_INGESTED_DIR: str = "ingested"
DATA_INGESTION_SPLIT_RATIO: float = 0.2

"""
Data Validation constants - starts with DATA_VALIDATION var name
"""
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = "validate"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


"""
Data Transformation constants - starts with DATA_TRANSORMATION var name
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_OBJECT_DIR: str = "transformed_object"


"""
Model Trainer constants - starts with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFITTING_THRESHOLD: float = 0.05


"""
Model Evaluation constants - starts with MODEL_EVALUATION var name
"""
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME = "report.yaml"

"""
Model Pusher constants - starts with MODEL_PUSHER var name
"""
MODEL_PUSHER: str = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR: str = SAVED_MODEL_DIR_NAME
