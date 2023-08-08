import os
import yaml
from ApsSensorFault.logging import log 
import numpy as np
import dill


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            log.info(f"yaml file loaded from {file_path}")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise e
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
            log.info(f"yaml file succefully edited at {file_path}")
    except Exception as e:
        raise e


def save_numpy_array_data(file_path: str, array = np.array):
    """
    save numpy array to data file
    file_path: location file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        log.exception(e)
        raise e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: location of file path
    return: np.array data load
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        log.exception(e)
        raise e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        log.info("Entered the save_obj of mainutil class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        log.info(f"dir created at {file_path} ")
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        log.info("exited the save_obj method of mailutil class")
    except Exception as e:
        log.exception(e)
        raise e