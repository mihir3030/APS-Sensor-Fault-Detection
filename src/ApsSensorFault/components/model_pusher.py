import os
import shutil
from ApsSensorFault.logging import log  
from ApsSensorFault.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from ApsSensorFault.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig
from ApsSensorFault.ml.metric.classification_metric import get_classification_score
from ApsSensorFault.ml.model.estimator import SensorModel
from ApsSensorFault.utils.main_util import save_object, load_object, write_yaml_file
from ApsSensorFault.ml.model.estimator import ModelResolver
from ApsSensorFault.constant.training_pipeline import TARGET_COLUMN


class ModelPusher:
    def __init__(self, model_eval_artifact: ModelEvaluationArtifact, model_pusher_config: ModelPusherConfig) -> None:
        try:
            self.model_eval_artifact = model_eval_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
           log.exception(e)
           raise e
        
    def initiate_model_pusher(self) -> ModelPusherConfig:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            
            shutil.copy(src=trained_model_path, dst=model_file_path)

            # for production
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=saved_model_path,
                model_file_path=model_file_path
            )

            return model_pusher_artifact

        except Exception as e:
            log.exception(e)
            raise e
        