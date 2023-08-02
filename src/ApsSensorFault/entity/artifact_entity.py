from dataclasses import dataclass

# output of data ingestion 
@dataclass
class DataIngestionArtifact:
    training_file_path: str
    testing_file_path: str