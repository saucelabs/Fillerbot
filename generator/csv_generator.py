from .generator import Generator,ListGenerator
import simpleeval
import random
import pandas as pd
import json

class CSVColumnGenerator(Generator):
    """
    CSVColumnGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(CSVColumnGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        
        self.data_list = list((pd.read_csv(data_item["csv_path"]))[data_item["column"]])
        self.data = data_item
        self.var_type = str(type(self.data).__name__)

    def generate(self,context=None):
        return random.choice(self.data_list)

    def size(self):
        return -1

    def serialize(self):
        o = super(CSVColumnGenerator, self).serialize()
        o['data'] = self.data
        return o
    
class CSVMultiColumnGenerator(Generator):
    """
    CSVMultiColumnGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(CSVMultiColumnGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        
        self.data_list = json.loads(((pd.read_csv(data_item["csv_path"],usecols=data_item["columns"])).drop_duplicates()).to_json(orient='records'))
        self.data = data_item
        self.var_type = str(type(self.data).__name__)

    def generate(self,context=None):
        return random.choice(self.data_list)

    def size(self):
        return -1

    def serialize(self):
        o = super(CSVMultiColumnGenerator, self).serialize()
        o['data'] = self.data
        return o