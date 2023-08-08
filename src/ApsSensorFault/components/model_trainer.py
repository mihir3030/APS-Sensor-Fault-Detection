import os
from xgboost import XGBClassifier

from ApsSensorFault.logging import log  
from ApsSensorFault.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from ApsSensorFault.entity.config_entity import ModelTrainerConfig
from ApsSensorFault.utils.main_util import load_numpy_array_data
from ApsSensorFault.ml.metric.classification_metric import get_classification_score
from ApsSensorFault.ml.model.estimator import SensorModel
from ApsSensorFault.utils.main_util import save_object, load_object


class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_trasformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            log.exception(e)
            raise e

    def train_model(self, x_train, y_train):
        try:
            xgb_classifier = XGBClassifier()
            xgb_classifier.fit(x_train, y_train)
            return xgb_classifier
        except Exception as e:
            log.exception(e)
            raise e
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            # loading our training adn testing array
            train_file_path = self.data_trasformation_artifact.transformed_train_file_path
            test_file_path = self.data_trasformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            # splitting data 
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            # train model
            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric = get_classification_score(y_train, y_train_pred)
            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("training accuracy is lower than threshold")

            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_test, y_test_pred)

            # overfitting and underfitting
            diff =abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            # 0.05 meanst 5% 
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception("model is overfitted")
            
            preprocessor = load_object(self.data_trasformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path)
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)
            save_obj = save_object(self.model_trainer_config.trained_model_file_path, sensor_model)

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric)
            return model_trainer_artifact
        
        except Exception as e:
            log.exception(e)
            raise e