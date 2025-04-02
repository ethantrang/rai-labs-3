import os
from pyairtable import Api
from dotenv import load_dotenv
load_dotenv()

class AirTableClient: 
    
    def __init__(
        self,
        api_key=os.environ['AIRTABLE_API_KEY'],
        base_id=os.environ['AIRTABLE_BASE_ID']
    ):   
        self.api = Api(api_key)
        self.base_id = base_id

    def read_all(self, table_name):
        return self.api.table(self.base_id, table_name).all()

    def create(self, data, table_name):
        return self.api.table(self.base_id, table_name).create(data)

    def update(self, record_id, data, table_name):
        return self.api.table(self.base_id, table_name).update(record_id, data)

    def delete(self, record_id, table_name):
        return self.api.table(self.base_id, table_name).delete(record_id)
        
db_client = AirTableClient()