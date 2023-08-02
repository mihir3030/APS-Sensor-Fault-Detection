import os
from ApsSensorFault.logging import log
from pandas import DataFrame
from ApsSensorFault.entity.config_entity import DataIngestionConfig
from ApsSensorFault.entity.artifact_entity import DataIngestionArtifact
from ApsSensorFault.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

   
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export Mongo DB Collection as DataFrame into Feature store
        """
        try:
            log.info("Exporting data from mongodb to feature store....")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(self.data_ingestion_config.collection_name)
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path)
            log.info(f"directory created at {dir_path}")

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            log.info(f"Dataset store at {feature_store_file_path} successsfully")

            return dataframe
        
        except Exception as e:
            log.exception(e)
            raise e

    def split_data_as_train_test_split(self, dataframe: DataFrame) -> None:
        """
        Feature Store data will be spliteed into train & test
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            log.info(f"Performed data split into train and test")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path)
            log.info(f"creating directory for saving train and test")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            log.info(f"training set succefully save at {self.data_ingestion_config.training_file_path}")

            test_set.to_csv(
                self.data_ingestion_config.tresting_file_path, index=False, header=True
            )
            log.info(f"testing set succefully save at {self.data_ingestion_config.tresting_file_path}")


        except Exception as e:
            log.exception(e)
            raise e

    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test_split(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path,
                                                            testing_file_path=self.data_ingestion_config.tresting_file_path)
            
            return data_ingestion_artifact
            
        except Exception as e:
            log.exception(e)
            raise e