import os
import pandas as pd
import numpy as np
from ApsSensorFault.constant.training_pipeline import SCHEMA_FILE_PATH
from ApsSensorFault.logging import log
from ApsSensorFault.entity.config_entity import DataValidationConfig
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from ApsSensorFault.utils.main_util import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            log.exception(e)
            raise e

    # for static methhod we can not use self
    @staticmethod   
    def read_data(filepath) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            log.exception(e)
            raise e
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            
            number_of_columns = len(self._schema_config['columns'])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            log.exception(e)
            raise e
        
    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns
            numerical_columns_present = True
            missing_numerical_columns = []
            for num_cols in numerical_columns:
                if num_cols not in dataframe_columns:
                    numerical_columns_present = False
                    
                    missing_numerical_columns.append(num_cols)
            
            return numerical_columns_present

        except Exception as e:
            log.exception(e)
            raise e

    # finding p_value 
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            log.info("checking data drift status...")
            report = {}
            status = True
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1, d2)
                if threshold<=is_same_distribution.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column: {
                        'pvalue': float(is_same_distribution.pvalue),
                        'drift_status': is_found
                    }
                })
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            log.info(f"dataset drift file stores at {drift_report_file_path}")

            return status

        except Exception as e:
            log.exception(e)
            raise e
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""
           
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.tested_file_path
            
            # read data from train and test from data ingestion
            train_dataframe = DataValidation.read_data(train_file_path)
            log.info(f"train data loading from data ingestion {train_file_path}")
            test_dataframe = DataValidation.read_data(test_file_path)
            log.info(f"test data loading from data ingestion {test_file_path}")

            # validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            
            if not status:
                error_message = f"{error_message} Training data set does not conatian all columns"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Testing data set does not conatian all columns"
            elif status:
                log.info(f"our scheme columns and dataframe columns count are matched")

            # validate numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} training set does not contain all numerical columns"
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} testing set does not contain all numerical columns"
            elif status:
                log.info("training and testing contain all numerical columns")

            if len(error_message)>0:
                raise Exception(error_message)
            
            elif len(error_message)<=0:
                log.info("train and test data are matching with our schema file")
                

            # check data drift
            """
            my name is mihir dholakia i am jr. data scitinst
            """
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.tested_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
                        
        except Exception as e:
            log.exception(e)
            raise e 