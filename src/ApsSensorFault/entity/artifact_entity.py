from dataclasses import dataclass

# output of data ingestion 
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    tested_file_path: str


# output of data validation
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

