from app.services.decorator_service import query_debugger
from app import db
import app.constants as Constants
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE, desc
from datetime import datetime,timedelta
from app.enums import EquipmentNames



class YardWriteService:
    def format_data_to_ccls_format(data):
        rake_data = {}
        if Constants.KEY_CONTAINER_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_NUMBER] = data[Constants.KEY_CONTAINER_NUMBER]
        if Constants.KEY_CONTAINER_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_CONTAINER_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S').isoformat()
        if Constants.ISO_CODE in data:
            rake_data[Constants.KEY_SOAP_ISO_CODE] = data[Constants.ISO_CODE]
        if Constants.KEY_CONTAINER_STAT in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_STAT] = data[Constants.KEY_CONTAINER_STAT] 
        if Constants.KEY_CONTAINER_SIZE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_SIZE] = data[Constants.KEY_CONTAINER_SIZE]
        if Constants.KEY_CONTAINER_TYPE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_TYPE] = data[Constants.KEY_CONTAINER_TYPE]
        if Constants.KEY_DAMAGE_FLAG in data:
            rake_data[Constants.KEY_SOAP_DAMAGE_FLAG] = data[Constants.KEY_DAMAGE_FLAG]
        if Constants.KEY_SEAL_STATUS in data:
            rake_data[Constants.KEY_SOAP_SEAL_STATUS] = data[Constants.KEY_SEAL_STATUS]
        if Constants.KEY_ATTRIBUTE1 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE1] = data[Constants.KEY_ATTRIBUTE1]
        if Constants.KEY_ATTRIBUTE2 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE2] = data[Constants.KEY_ATTRIBUTE2]
        if Constants.KEY_ATTRIBUTE3 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE3] = data[Constants.KEY_ATTRIBUTE3]
        if Constants.KEY_ATTRIBUTE4 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE4] = data[Constants.KEY_ATTRIBUTE4]
        if Constants.KEY_ATTRIBUTE5 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE5] = data[Constants.KEY_ATTRIBUTE5]
        if Constants.KEY_ATTRIBUTE6 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE6] = datetime.strptime(data[Constants.KEY_ATTRIBUTE6], '%Y-%m-%d %H:%M:%S').isoformat()
        if Constants.KEY_ATTRIBUTE7 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE7] = datetime.strptime(data[Constants.KEY_ATTRIBUTE7], '%Y-%m-%d %H:%M:%S').isoformat()
        if Constants.KEY_CREATED_AT in data:
            rake_data[Constants.KEY_SOAP_CREATED_AT] = datetime.strptime(data[Constants.KEY_CREATED_AT], '%Y-%m-%d %H:%M:%S').isoformat()
        if Constants.KEY_CREATED_BY in data:
            rake_data[Constants.KEY_SOAP_CREATED_BY] = data[Constants.KEY_CREATED_BY]
        if Constants.KEY_UPDATED_AT in data:
            rake_data[Constants.KEY_SOAP_UPDATED_AT] = datetime.strptime(data[Constants.KEY_UPDATED_AT], '%Y-%m-%d %H:%M:%S').isoformat()
        if Constants.KEY_UPDATED_BY in data:
            rake_data[Constants.KEY_SOAP_UPDATED_BY] = data[Constants.KEY_UPDATED_BY]
        if Constants.KEY_ERROR_MSG in data:
            rake_data[Constants.KEY_SOAP_ERROR_MSG] = data[Constants.KEY_ERROR_MSG]
        if Constants.KEY_STATUS_FLG in data:
            rake_data[Constants.KEY_SOAP_STATUS_FLG] = data[Constants.KEY_STATUS_FLG]
        if Constants.KEY_READ_FLG in data:
            rake_data[Constants.KEY_SOAP_READ_FLG] = data[Constants.KEY_READ_FLG]
        if "from_location" in data:
            rake_data[Constants.KEY_SOAP_FROM_LOC] = data["from_location"]
        if "to_location" in data:
            rake_data[Constants.KEY_SOAP_TO_LOC] = data["to_location"]
        if "stack_location" in data:
            rake_data[Constants.KEY_SOAP_STACK_LOC] = data["stack_location"]
        if "icd_location" in data:
            rake_data[Constants.KEY_SOAP_ICD_LOC_CODE] = data["icd_location"]
        if "trailer_number" in data:
            rake_data[Constants.KEY_SOAP_TRAILER_NUMBER] = data["trailer_number"]
        if "operation_time" in data:
            rake_data[Constants.KEY_SOAP_OPERATION_TIME] = datetime.strptime(data["operation_time"], '%Y-%m-%d %H:%M:%S').isoformat()
        if "seal_date" in data:
            rake_data[Constants.KEY_SOAP_SEAL_DATE] = datetime.strptime(data["seal_date"], '%Y-%m-%d %H:%M:%S').isoformat()
        return rake_data
    
    def dtms_yard_write_format(data):
        return YardWriteService.format_data_to_ccls_format(data)

    def exim_yard_write_format(data): 
        yard_data = YardWriteService.format_data_to_ccls_format(data)
        # Pushing dummy data
        if Constants.KEY_TRAIN_NUMBER in data:
            yard_data[Constants.KEY_SOAP_TRAIN_NUMBER] = data[Constants.KEY_TRAIN_NUMBER]
        else:
            yard_data[Constants.KEY_SOAP_TRAIN_NUMBER] = "TGS601809"
        if not Constants.KEY_SOAP_CREATED_AT in yard_data:
            yard_data[Constants.KEY_SOAP_CREATED_AT] = datetime.now().isoformat()
        if not Constants.KEY_SOAP_UPDATED_AT in yard_data:
            yard_data[Constants.KEY_SOAP_UPDATED_AT] = datetime.now().isoformat()
        if not Constants.KEY_SOAP_SEAL_DATE in yard_data:
            yard_data[Constants.KEY_SOAP_SEAL_DATE] = datetime.now().isoformat()
        if not Constants.KEY_SOAP_UPDATED_BY in yard_data:
            yard_data[Constants.KEY_SOAP_UPDATED_BY ] = "ctms_user"

        return yard_data
