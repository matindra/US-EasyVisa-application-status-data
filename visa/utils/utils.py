import yaml
import os, sys
import numpy as np
import pandas as pd
from visa.constant import *
from visa.exception import CustomException



def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys) from e
