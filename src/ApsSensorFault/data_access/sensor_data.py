import pandas as pd
import numpy as np
from typing import Optional
from ApsSensorFault.configuration.mongo_db_connection import MongoDBClient
from ApsSensorFault.constant.database import DATABASE_NAME
from ApsSensorFault.logging import log 

class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            log.exception(e)
            raise e
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str]=None) -> pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop(columns=['_id'], axis=1, inplace=True)
            df.replace({'na':np.nan}, inplace=True)
            log.info(f"data exported succefully from mongodb to dataframe")
            return df
            
        except Exception as e:
            log.exception(e)
            raise e
