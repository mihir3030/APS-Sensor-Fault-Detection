import os
from ApsSensorFault.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from ApsSensorFault.logging import log
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from ApsSensorFault.components.data_ingestion import DataIngestion
from ApsSensorFault.components.data_validation import DataValidation
from ApsSensorFault.components.data_transformation import DataTransformation
from ApsSensorFault.components.model_trainer import ModelTrainer
from ApsSensorFault.components.model_evaluation import ModelEvaluation
from ApsSensorFault.components.model_pusher import ModelPusher

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
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            log.info(f">>>>>>>>>>>>>>>>> Data transformation Stage started")
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

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            log.info(f">>>>>>>>>>>>>>>>> Model Trainer Stage started")
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.trainig_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            log.info(f"model trainer compleated at {model_trainer_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Model Trainer Stage compleated successfully\n")

            return model_trainer_artifact
        except Exception as e:
            log.exception(e)
            raise e

    def start_model_evaluation(self, data_validation_artifact: DataValidationArtifact, 
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            log.info(f">>>>>>>>>>>>>>>>> Model Evaluation Stage started")
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.trainig_pipeline_config)
            model_evaluation = ModelEvaluation(data_validation_artifact=data_validation_artifact,
                                               model_trainer_artifact=model_trainer_artifact,
                                               model_evaluation_config=model_evaluation_config)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            log.info(f"model evaluation compleated at {model_evaluation_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Model Evaluation Stage compleated successfully\n")
            return model_evaluation_artifact
        
        except Exception as e:
            log.exception(e)
            raise e

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            log.info(f">>>>>>>>>>>>>>>>> Model Pusher Stage started")
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.trainig_pipeline_config)
            model_pusher = ModelPusher(model_eval_artifact=model_evaluation_artifact, model_pusher_config=model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            log.info(f"model pusher compleated at {model_pusher_artifact}")
            log.info(f">>>>>>>>>>>>>>>>> Model Pusher Stage compleated successfully\n")
            return model_pusher_artifact
        
        except Exception as e:
            log.exception(e)
            raise e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact2 = self.start_data_ingestion()
            # print(f"222222 = {data_ingestion_artifact2}")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact2)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception(f"Trained Model is better than best model")
            
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact) 
        except Exception as e:
            log.exception(e)
            raise e
        