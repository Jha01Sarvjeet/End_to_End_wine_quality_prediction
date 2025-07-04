import os
from src.wine_qulity_predction import logger
import pandas as pd
from sklearn.model_selection import train_test_split
from src.wine_qulity_predction.config.configuration import DataTransformationConfig
class DataTransformation:
    def __init__(self,config: DataTransformationConfig):
        self.config=config
    
    def train_test_splitting(self):
        data=pd.read_csv(self.config.data_path)
        
        #splitting the data into train test 
        train,test=train_test_split(data)
        
        train.to_csv(os.path.join(self.config.root_dir,'train.csv'),index=False)
        test.to_csv(os.path.join(self.config.root_dir,'test.csv'),index=False)
        
        logger.info('splitted the data into train test set')
        logger.info(train.shape)
        logger.info(test.shape)
        
        
