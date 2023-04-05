from app.constants import GroundTruthType
from app.services.decorator_service import query_debugger
from app.services import soap_service
from app.services.rake.gt_upload_service import commit
from app.logger import logger
import app.constants as Constants
import config
import time
from datetime import datetime



class RakeOutwardWriteService():
    def format_data_to_ccls_format(data):
        rake_data = {}
        if  Constants.KEY_TRAIN_NUMBER in data :
            rake_data[Constants.KEY_SOAP_TRAIN_NUMBER] = data[Constants.KEY_TRAIN_NUMBER]
        else :
            rake_data[Constants.KEY_SOAP_TRAIN_NUMBER] = "TEST_TRAIN"
        if Constants.KEY_DT_DESP in data:
            rake_data[Constants.KEY_SOAP_DT_DESP] = datetime.strptime(data[Constants.KEY_DT_DESP], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_RAKE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_RAKE_NUMBER] = data[Constants.KEY_RAKE_NUMBER]
        if Constants.KEY_HLD_TRACK_NUMBER in data:
            rake_data[Constants.KEY_SOAP_HLD_TRACK_NUMBER] = data[Constants.KEY_HLD_TRACK_NUMBER]
        if Constants.KEY_DT_WTR in data:
            rake_data[Constants.KEY_SOAP_DT_WTR] = datetime.strptime(data[Constants.KEY_DT_WTR], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_EQUIPMENT_ID in data:
            rake_data[Constants.KEY_SOAP_EQUIPMENT_ID] = data[Constants.KEY_EQUIPMENT_ID]
        if Constants.KEY_GATEWAY_PORT_CD in data:
            rake_data[Constants.KEY_SOAP_GATEWAY_PORT_CD] = data[Constants.KEY_GATEWAY_PORT_CD]
        if Constants.KEY_CONTAINER_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_NUMBER] = data[Constants.KEY_CONTAINER_NUMBER]
        if Constants.KEY_CONTAINER_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_CONTAINER_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_WAGON_NUMBER in data:
            rake_data[Constants.KEY_SOAP_WAGON_NUMBER] = data[Constants.KEY_WAGON_NUMBER]
        if Constants.KEY_WAGON_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_WAGON_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_WAGON_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_WAGON_TYPE in data:
            rake_data[Constants.KEY_SOAP_WAGON_TYPE] = data[Constants.KEY_WAGON_TYPE]
        if Constants.KEY_DAMAGE_FLAG in data:
            rake_data[Constants.KEY_SOAP_DAMAGE_FLAG] = data[Constants.KEY_DAMAGE_FLAG]
        if Constants.KEY_SLINE_CODE in data:
            rake_data[Constants.KEY_SOAP_SLINE_CODE] = data[Constants.KEY_SLINE_CODE]
        if Constants.ISO_CODE in data:
            rake_data[Constants.KEY_SOAP_ISO_CODE] = data[Constants.ISO_CODE]
        if Constants.KEY_CONTAINER_SIZE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_SIZE] = data[Constants.KEY_CONTAINER_SIZE]
        if Constants.KEY_CONTAINER_TYPE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_TYPE] = data[Constants.KEY_CONTAINER_TYPE]
        if Constants.KEY_CONTAINER_STAT in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_STAT] = data[Constants.KEY_CONTAINER_STAT] 
        if Constants.KEY_CONTAINER_WEIGHT in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_WEIGHT] = data[Constants.KEY_CONTAINER_WEIGHT]
        if Constants.KEY_FIRST_POD in data:
            rake_data[Constants.KEY_SOAP_FIRST_POD] = data[Constants.KEY_FIRST_POD]
        if Constants.KEY_ORIGIN_STATION in data:
            rake_data[Constants.KEY_SOAP_ORIGIN_STATION] = data[Constants.KEY_ORIGIN_STATION]
        if Constants.KEY_DEST_STATION in data:
            rake_data[Constants.KEY_SOAP_DEST_STATION] = data[Constants.KEY_DEST_STATION]
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
            rake_data[Constants.KEY_SOAP_ATTRIBUTE6] = datetime.strptime(data[Constants.KEY_ATTRIBUTE6], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_ATTRIBUTE7 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE7] = datetime.strptime(data[Constants.KEY_ATTRIBUTE7], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_CREATED_AT in data:
            rake_data[Constants.KEY_SOAP_CREATED_AT] = datetime.strptime(data[Constants.KEY_CREATED_AT], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_CREATED_BY in data:
            rake_data[Constants.KEY_SOAP_CREATED_BY] = data[Constants.KEY_CREATED_BY]
        if Constants.KEY_UPDATED_AT in data:
            rake_data[Constants.KEY_SOAP_UPDATED_AT] = datetime.strptime(data[Constants.KEY_UPDATED_AT], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_UPDATED_BY in data:
            rake_data[Constants.KEY_SOAP_UPDATED_BY] = data[Constants.KEY_UPDATED_BY]
        if Constants.KEY_ERROR_MSG in data:
            rake_data[Constants.KEY_SOAP_ERROR_MSG] = data[Constants.KEY_ERROR_MSG]
        if Constants.KEY_STATUS_FLG in data:
            rake_data[Constants.KEY_SOAP_STATUS_FLG] = data[Constants.KEY_STATUS_FLG]
        if Constants.KEY_READ_FLG in data:
            rake_data[Constants.KEY_SOAP_READ_FLG] = data[Constants.KEY_READ_FLG]
        if "equipment_name" in data:
            rake_data[Constants.KEY_SOAP_EQUIPMENT_ID] = data["equipment_name"]
        return rake_data
        

    
    @query_debugger()
    def update_CGO_survey(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                ccls_data = RakeOutwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_outward_rake(ccls_data,Constants.CGO_SURVEY_ENDPOINT)
                return result
            return {}
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeOutwardWriteService.update_CGO_survey(data,count)
                
    
    @query_debugger()
    def update_outward_train_summary(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                request_data = RakeOutwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_outward_rake(request_data,Constants.UPDATE_OUTWARD_WTR_ENDPOINT)
                return result
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeOutwardWriteService.update_outward_rake_details(count=count,isRetry=Constants.KEY_RETRY_VALUE)
