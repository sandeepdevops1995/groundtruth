from datetime import datetime, timezone
import time
from sqlalchemy.types import TypeDecorator, DateTime
import json


# To convert dict and list to string (to strictly use it as SQL db)
def db_format(data):
    for value in data:
        if isinstance(data[value],dict):
            data[value] = json.dumps(data[value])
        elif isinstance(data[value],list):
            data[value] = json.dumps(data[value])
    return data


# To converts models to json or dict format
class db_functions():
    def __init__(self,data):
        self.data = data
        if isinstance(data,list):
            self.many = True
        else:
            self.many = False
        
    def as_dict(self):
        def dict_data(table):
            return {c.name: getattr(table, c.name) for c in table.__table__.columns}
            
        if self.many:
            final_data = []
            for table in self.data:
                final_data.append(dict_data(table))
            return final_data
        else:
           return dict_data(self.data) 
    
    def as_json(self):
        def json_data(table):
            data = {}
            for c in table.__table__.columns:
                value = getattr(table, c.name)
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except:
                        pass
                data[c.name] = value
            return data
    
        if self.many:
            
            final_data = []
            for table in self.data:
                final_data.append(json_data(table))
            return json.dumps(final_data)
        else:
            return json.dumps(json_data(self.data))
        
 
class IntegerDateTime(TypeDecorator):
    """a type that decorates DateTime, converts to unix time on
    the way in and to datetime.datetime objects on the way out."""
    impl = DateTime
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo
    def process_bind_param(self, value, engine):
        # print("int(value)--------------",int(value))
        value = datetime.fromtimestamp(int(value)/1000)
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(timezone.utc)
    # def process_result_value(self, value, engine):
    #     """Assumes a datetime.datetime"""
    #     assert isinstance(value, datetime)
    #     return int(time.mktime(value.timetuple()))
    # def copy(self):
    #     return IntegerDateTime(timezone=self.timezone)
    
