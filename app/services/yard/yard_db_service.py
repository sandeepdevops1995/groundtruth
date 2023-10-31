from app.services.decorator_service import query_debugger
from app.services.soap_service import *
from app.services.gate.database_service import GateDbService
from app.services.yard.yard_write import YardWriteService
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
                if "equipment_id" in data and data["equipment_id"]:
                    data["attribute1"] = EquipmentNames[data["equipment_id"]].value if EquipmentNames[data["equipment_id"]].value else "CHE"
                trans_type = data.pop("trans_type","EXIM")
                if trans_type == "DOM":
                    dtms_data = YardWriteService.dtms_yard_write_format(data) 
                    result =  update_domestic_container_stack_location(dtms_data)
                else:
                    ccls_data = YardWriteService.exim_yard_write_format(data)
                    result =  update_container_stack_location(ccls_data)
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
    
    def get_domestic_container_details(container_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
               pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                data = {"ctr_number":container_number}
                response  = get_domestic_yard_container_details(data)
                result = YardDbService.format_domestic_container_details(response)
                return result
        except Exception as e:
            logger.exception('Get Domestic Container Details, Exception : '+str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                YardDbService.get_domestic_container_details(data,count)
        return{}

    def format_domestic_container_details(ccls_data):
        data = {}
        data["terminal_code"] = ccls_data["davtrmncode"]
        data["container_number"] = ccls_data["daccntrnumb"]
        data["container_size"] = ccls_data["dancntrsize"]
        data["container_type"] = ccls_data["daccntrtype"]
        data["loaded_empty_flag"] = ccls_data["dacleflag"]
        data["container_special_flag"] = ccls_data["daccntrspclflag"]
        data["stack_location"] = ccls_data["dacstcklocn"]
        data["prev_stack_location"] = ccls_data["dacprevstcklocn"]
        data["ISO_DSO_flag"] = ccls_data["dacisodsoflag"]
        data["crntstts"] = ccls_data["daccrntstts"]
        data["crntstts_time"] = ccls_data["dadcrntsttstime"].strftime("%Y-%m-%dT%H:%M:%S")
        data["prvsstts"] = ccls_data["davprvsstts"]
        data["csf_code"] = ccls_data["dacsfcode"]
        data["cbtgstrg_flag"] = ccls_data["daccbtgstrgflag"]
        data["container_weight"] = float(ccls_data["dancntrcc"])
        data["container_tare_weight"] = float(ccls_data["dancntrtare"])
        data["seal_number"] = ccls_data["dannumbseal"]
        data["handling_over_date"] = ccls_data["dadhndgoverdate"].strftime("%Y-%m-%dT%H:%M:%S")
        data["sline_code"] = ccls_data["dacshiplinecode"]
        data["vldt_flag"] = ccls_data["dacvldtflag"]
        data["container_owner_flag"] = ccls_data["daccntrownerflag"]