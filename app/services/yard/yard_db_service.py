from app.services.decorator_service import query_debugger
from app.services.soap_service import *
from app.services.gate.database_service import GateDbService
from app.models import KyclContainerLocation
from app.logger import logger
from app.constants import GroundTruthType
import app.constants as Constants
from app import engine as e
from sqlalchemy.sql import text
import time
import config
import os

class YardDbService:
    @query_debugger()
    def get_master_data(self,sql_filename,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            print("sql file ",sql_filename)
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,sql_filename))
            command = text(sqlFile.read())
            query = conn.execute(command)
            sqlFile.close()
            conn.close()
            data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            return json.dumps(data)
        except Exception as e:
            logger.exception('Update Container Location, Exception : '+str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                self.get_master_data(sql_filename,count)
    
    @query_debugger()
    def update_container_location(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                data["stk_loc"] = data["stack_location"]
                result = GateDbService().update_ctr_stack_info(data)
                return result
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                # updating stack location based on it's value
                if "from_location" in data and data["from_location"]:
                    data["from_location"] = YardDbService.get_stack_location(data["from_location"])
                if "to_location" in data and data["to_location"]:
                    data["to_location"] = YardDbService.get_stack_location(data["to_location"])
                result =  update_container_stack_location(data)
                if result:
                    return result
            container_location = KyclContainerLocation(container_no = data["container_number"] ,to_loc = data["stack_location"] )
            db.session.add(container_location)
            if commit():
                return {"message" : "saved in postgres db"}

        except Exception as e:
            logger.exception('Update Container Location, Exception : '+str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                YardDbService.update_container_location(data,count)

        
    def get_stack_location(stack_location):
        if stack_location == "Truck":
            return  "TT"
        elif stack_location == "Lane":
            return "WHF"
        elif stack_location == "Track":
            return "RS"
        return stack_location

        
        
