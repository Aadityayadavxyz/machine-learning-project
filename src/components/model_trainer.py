import os 
import sys
from dataclasses import dataclass
from catboost import catboostregresser
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_model,save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Splitting training and test input data')
            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = (
                'Random Forrest': RandomForestClassifier(),
                'Decision Tree' : DecisionTreeClassifier(),
                'Gradient boosting' : GradientBoostingClassifier(),
                'Logistic regressor' : LogisticRegression(),
                'KNN' : KNeighborsClassifier(),
                'XGBClassifier' : XGBClassifier(),
                'Cat boost classifier'  : CatBoostClassifier(),
                'Ada Boost classifier' : AdaBoostClassifier()
                )
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }

            model_report:dict = evaluate_model(
                x_train=x_train,
                y_train = y_train,
                x_test=x_test,
                y_test=y_test,
                models=models
                params = params
            )
            
            best_model_score = max(list(model_report.values()))
            best_model = list(model_report.keys())[list(model_report.values()).index(best_model)]
            
            if best_model_score<0.6:
                raise CustomException('no best model found')
            logging.info('Best model found')
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
                                                 
            predicted = best_model.predict(x_test)
            r2_score = r2_score(y_test, predicted)
            return r2_score
        
            
        except Exception as e:
            raise CustomException(e,sys)
        logging.info('Initializing model training')