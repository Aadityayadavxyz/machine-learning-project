# #import pandas as pd
# import os
# import sys
# from dotenv import load_dotenv
# from src.logger import logging 
# #load_dotenv()
# #host = os.getenv('host')
# #user = os.getenv('user')
# #password = os.getenv('password')
# #db = os.getenv('db')
import sys
import os
from src.exception import CustomException
# #def read_sql_data():
#     logging.info('Reading sql database started')
#     mydb = pymysql.connect(
#         host = host,
#         user = user,
#         password = password,
#         db = db
#     )
#     df = mydb.read_sql_query('select * from db',mydb)
#     print(df.head(5))
#     return df
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)