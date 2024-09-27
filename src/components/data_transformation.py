import os
import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_filepath = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['','','','']
            categorical_columns = ['','','','','']
            
            num_pipeline = Pipeline(steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler)])
            
            cat_pipeline = Pipeline(steps =[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoding',OneHotEncoder),
                    ('scaler',StandardScaler)])
            
            logging.info('Numerical columns standard scaling and imputation done')
            logging.info('Categorical columns standard scaling,imputation and one hot encoding done')
            
            preprocessor = ColumnTransformer([
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)])
            return preprocessor
        

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read the train and test dataframes from file paths")
            processing_obj = self.get_data_transformer_object()
            target_column_name = ['']
            
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            input_feature_train_arr = processing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr =  processing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("Finally train and test array made")
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_filepath,
                obj = processing_obj
            )
            return (train_arr, test_arr,self.data_transformation_cofig.preprocessor_obj_filepath)
        
        except Exception as e:
            raise CustomException(e,sys)