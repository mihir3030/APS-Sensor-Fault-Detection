import os
from ApsSensorFault.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from ApsSensorFault.logging import log
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from ApsSensorFault.components.data_ingestion import DataIngestion
from ApsSensorFault.components.data_validation import DataValidation
from ApsSensorFault.components.data_transformation import DataTransformation

class TrainingPipeline:
    def __init__(self):
        self.trainig_pipeline_config = TrainingPipelineConfig()
        #self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.trainig_pipeline_config)

    def start_data_ingestion(self):
        try:
            log.info(f">>>>>>>>>>>>>>>>> Data Ingestion Stage started")
            
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.trainig_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            log.info(f"data ingesion compleated at {data_ingestion_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Data Ingestion Stage compleated successfully\n")
            return data_ingestion_artifact
            
        except Exception as e:
            log.exception(e)
            raise e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            log.info(f">>>>>>>>>>>>>>>>> Data Validation Stage started")
            data_validation_config = DataValidationConfig(self.trainig_pipeline_config)
            data_Validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            data_validation_artifact = data_Validation.initiate_data_validation()
            log.info(f"data validation compleated at {data_validation_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Data Validation Stage compleated successfully\n")
            return data_validation_artifact
            
        except Exception as e:
            log.exception(e)
            raise e
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            log.info(f">>>>>>>>>>>>>>>>> Data Validation Stage started")
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.trainig_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                      data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            log.info(f"data transformation compleated at {data_transformation_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Data transformation Stage compleated successfully\n")
            
            return data_transformation_artifact

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
            data_ingestion_artifact2 = self.start_data_ingestion()
            # print(f"222222 = {data_ingestion_artifact2}")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact2)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact) 
        except Exception as e:
            log.exception(e)
            raise e
        