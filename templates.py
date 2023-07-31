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

