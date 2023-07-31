import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

package_name = "ApsSensorFault"

list_of_files = [
    '.github/workflows/.gitkeep',
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/configuration/__init__.py",
    f"src/{package_name}/entity/__init__.py",
    f"src/{package_name}/entity/artifact_entity.py", # decide to how many artifacts will save
    f"src/{package_name}/entity/config_entity.py", # decide what input to our component files 
    f"src/{package_name}/constant/__init__.py",
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/components/data_ingestion.py",
    f"src/{package_name}/components/data_validation.py",
    f"src/{package_name}/components/data_transformation.py",
    f"src/{package_name}/components/model_trainer.py",
    f"src/{package_name}/components/model_evaluations.py",
    f"src/{package_name}/pipeline/__init__.py",
    f"src/{package_name}/pipeline/training_pipeline.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/logging.py",
    f"src/{package_name}/exception.py",
    f"src/{package_name}/data_access/__init__.py", # read data from mongodb and save to current
    f"src/{package_name}/cloud_storage/__init__.py", # all the code related to cloud get and upload to s3
    f"src/{package_name}/ml/__init__.py", # Create some custome function like - custom loss function
    "configs/config.yaml",
    "params.yaml",
    "requirements.txt",
    "requirements-dev.txt",
    "setup.py"
]

for file_path in list_of_files:
    filepath = Path(file_path)
    filedir, filename = os.path.split(filepath)
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"creating {filedir} for {filepath}")
    
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            pass
        logging.info(f"file {filename} successfully created")

