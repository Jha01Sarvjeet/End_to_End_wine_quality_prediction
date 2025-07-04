import os
import sys
import yaml
from src.wine_qulity_predction import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError



@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    """
    reads Yaml file and return

    Args:
        path_to_yaml(str):path like input

    Raises:
        ValueError:if Yaml file is empty
        e:empty file
    Returns:
        ConfigBox: ConfigBox type

    """

    try:
        with open(path_to_yaml) as yaml_file:
            content=yaml.safe_load(yaml_file)
            logger.info(f"yaml file : {path_to_yaml} loadded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories:list,verbose = True):
    '''
    create list of directories

    Args:
        path_to_directories(list): list of path of directories
        verbose (bool, optional): If True, logs directory creation. Defaults to True.
    '''

    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"Created directory at {path}")


@ensure_annotations
def save_json(path: Path,data: dict):
    '''
    save json

    Args:
        path(Path)L: path to json file
        data(dict): data to be saved in json file
    '''

    with open(path,'w') as f: 
        json.dump(data,f,indent=4)

    logger.info(f'json file saved at {path}')


@ensure_annotations
def load_json(path:Path)->ConfigBox:
     """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
     with open(path) as f:
         content = json.load(f)

     logger.log("json file successfully loaded from {path}")
     return ConfigBox(content)


@ensure_annotations
def save_bin(data:Any,path:Path):

    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data,filename=path)
    logger.info(f"binary file saved at: {path}")



@ensure_annotations
def laod_bin(data:Any,path:Path)->Any:

    """load binary file

    Args:
        path (Path): path to binary file

    Return:
         Any: object stored in the file
    """
    data=joblib.load(filename=path)
     
    logger.info(f"binary file saved at: {path}")
    return data
    
        