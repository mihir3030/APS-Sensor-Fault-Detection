from dataclasses import dataclass

# dataclass you don't have to use __init__() it will automatically create instance
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


# output of data transformation
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


# output of model trainer classification score
@dataclass
class ClassificationMatricArtifact:
    f1_score: float
    precision_score: float
    recall_Score: float


# output of model trainer 
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: str
    test_metric_artifact: str

    
# output of model evaluation
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    trained_model_metric_artifact: ClassificationMatricArtifact
    best_model_metric_artifact: ClassificationMatricArtifact 


# output of model pusher
@dataclass
class ModelPusherArtifact:
    saved_model_path: str
    model_file_path: str 
