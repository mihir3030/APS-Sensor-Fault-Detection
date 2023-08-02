import os, sys
from ApsSensorFault.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from ApsSensorFault.logging import log
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        self.trainig_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.trainig_pipeline_config)

    def start_data_ingestion(self):
        try:
            log.info(f">>>>>>>>>>>>>>>>> Data Ingestion Stage started")
            log.info(f">>>>>>>>>>>>>>>>> Data Ingestion Stage compleated successfully compleated\n")
        except Exception as e:
            log.exception(e)
            raise e
        
    def start_data_validation(self) -> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            log.exception(e)
            raise e
        
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            log.exception(e)
            raise e

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            log.exception(e)
            raise e

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            log.exception(e)
            raise e

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            log.exception(e)
            raise e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            log.exception(e)
            raise e
        