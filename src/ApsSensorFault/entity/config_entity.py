import os
from datetime import datetime
from ApsSensorFault.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = training_pipeline.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config=TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_STORE_DIR_NAME, training_pipeline.FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTED_INGESTED_DIR, training_pipeline.TRAINING_FILE_NAME
        )
        self.tresting_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTED_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME