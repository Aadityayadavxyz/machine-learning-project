import os
import sys
import pandas as pd
from dataclasses import dataclass
from logger import logging
from sklearn.model_selection import train_test_split
from exception import CustomException
@dataclass
class dataingestionconfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')
    
class dataingestion:
    def __init__(self):
        self.ingestion_config = dataingestionconfig()
    def initiate_data_ingestion(self):
        logging.info('Entered the data ingestion')
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the data as dataframe')
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info('Train Test split initalization')
            train_set,test_set = train_test_split(df,test_size=0.2)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info('Train test split done and respective datasets are saved to the files')
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
            