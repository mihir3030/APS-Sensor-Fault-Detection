import pandas as pd
import os
import numpy as np
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from ApsSensorFault.constant.training_pipeline import TARGET_COLUMN
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from ApsSensorFault.logging import log
from ApsSensorFault.entity.config_entity import DataTransformationConfig
from ApsSensorFault.utils.main_util import save_numpy_array_data, load_numpy_array_data, save_object
from ApsSensorFault.ml.model.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        """
        dat_validation_artifact: Output refrence of data ingestion artifact stage
        data_transformation_config: Configuration of data transformation stage
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_trasformation_config = data_transformation_config
        except Exception as e:
            log.exception(e)
            raise e
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            log.exception(e)
            raise e
    
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            robust_scaler = RobustScaler()

            preprocessor = Pipeline(
                steps=[
                    ("imputer", simple_imputer),
                    ("RobustScaler", robust_scaler)]
            )

            return preprocessor
        except Exception as e:
            raise (e)


    def initiate_data_transformation(self):
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            log.info(f"train data loading from data ingestion {self.data_validation_artifact.valid_train_file_path}")
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            log.info(f"train data loading from data ingestion {self.data_validation_artifact.valid_test_file_path}")
            preprocesser = self.get_data_transformer_object()

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            log.info(f"target class converted to integer")

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            preprocesser_obj = preprocesser.fit(input_feature_train_df)
            transformed_input_train_feature = preprocesser_obj.transform(input_feature_train_df)
            log.info(f"train data null value filled from simple inputer and data scaled from Robust scaler")
            transformed_input_test_feature = preprocesser_obj.transform(input_feature_test_df)
            log.info(f"test data null value filled from simple inputer and data scaled from Robust scaler")


            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_train_feature, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                transformed_input_test_feature, target_feature_test_df
            )
            log.info(f"handled imbalanced train & test data using Smote OverSampling")

            train_array = np.c_[input_feature_train_final, np.array(target_feature_train_final)]

            test_array = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            log.info(f"train and test data converted into numpy array")

            # save numpy array data
            save_numpy_array_data(self.data_trasformation_config.transformed_train_file_path, array=train_array)
            save_numpy_array_data(self.data_trasformation_config.transformed_test_file_path, array=test_array)
            log.info(f"saved train numpy array data at {self.data_trasformation_config.transformed_train_file_path}")
            log.info(f"saved test numpy array data at {self.data_trasformation_config.transformed_test_file_path}")



            save_object(self.data_trasformation_config.transformed_object_file_path, obj=preprocesser_obj)
            log.info(f"saved preprocess object pkl file at {self.data_trasformation_config.transformed_object_file_path}")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_trasformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_trasformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_trasformation_config.transformed_test_file_path
            )

            return data_transformation_artifact


           

        except Exception as e:
            log.exception(e)
            raise e

    