import sys
import pandas as pd
from app.main.exception import CustomException
from app.main.logging import logging
from app.db_models import ContactTable
from app import db
from datetime import datetime

class CustomData:
    def __init__(self, 
        name: str,
        email:str,
        subject: str,
        message: str,
        date: datetime = None):

        self.name=name
        self.email=email
        self.subject=subject
        self.message=message
        self.date = date if date is not None else datetime.now()
       
               

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "name": [self.name],
                "email": [self.email],
                "subject": [self.subject],
                "message": [self.message],
                "date": [self.date],
                                
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def add_to_database(self, df):
        try:
            # Convert DataFrame to list of dictionaries
            data_dicts = df.to_dict(orient='records')

            # Bulk insert using SQLAlchemy
            db.session.bulk_insert_mappings(ContactTable, data_dicts)
            db.session.commit()
        except Exception as e:
            raise CustomException(e, sys)
            db.session.rollback()