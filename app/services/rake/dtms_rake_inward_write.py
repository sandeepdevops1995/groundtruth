from app.services.decorator_service import query_debugger
from app.models import  WgnMst, MissedInwardContainers, DomesticContainers
from app import db
from app.constants import GroundTruthType
import app.constants as Constants
from app.services import soap_service
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE, desc
from datetime import datetime,timedelta
import config
import json
import time


class DTMSRakeInwardWriteService:
    def format_data_to_ccls_format(data):
        rake_data = {}
        rake_data["trainNumber"] = "TEST"
        if  Constants.KEY_TRAIN_NUMBER in data :
            rake_data["trainNumber"] = data[Constants.KEY_TRAIN_NUMBER] if data[Constants.KEY_TRAIN_NUMBER] else "TEST"
        if  Constants.KEY_ORIGIN_STATION in data:
            rake_data["origionStation"] = data[Constants.KEY_ORIGIN_STATION]
        if Constants.KEY_CONTAINER_NUMBER in data:
            rake_data["containerNumber"] = data[Constants.KEY_CONTAINER_NUMBER]
        if Constants.KEY_SLINE_CODE in data:
            rake_data["slineCode"] = data[Constants.KEY_SLINE_CODE]
        if Constants.KEY_CONTAINER_SIZE in data:
            rake_data["containerSize"] = float(data[Constants.KEY_CONTAINER_SIZE])
        if Constants.KEY_CONTAINER_TYPE in data:
            rake_data["containerType"] = data[Constants.KEY_CONTAINER_TYPE]
        if Constants.KEY_WAGON_NUMBER in data:
            rake_data["wagonNumber"] = float(data[Constants.KEY_WAGON_NUMBER])
        if Constants.KEY_SEAL_NUMBER in data:
            rake_data["sealNumber"] = data[Constants.KEY_SEAL_NUMBER]
        if Constants.KEY_CONTAINER_STAT in data:
            rake_data["containerStatus"] = data[Constants.KEY_CONTAINER_STAT]
        if Constants.KEY_HAZARD_STATUS in data:
            rake_data[Constants.KEY_SOAP_HAZARD_STATUS] = data[Constants.KEY_HAZARD_STATUS]        
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
        return rake_data
    

    # TODO: Equipment ID is not available. So this function is not using any where
    @query_debugger()
    def update_container(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                ccls_data = DTMSRakeInwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_domestic_inward_rake(ccls_data,Constants.UPDATE_RAKE_CONTAINER_ENDPOINT)
                return result
            return {}
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                DTMSRakeInwardWriteService.update_container(data,count)

    @query_debugger()
    def update_VGI_survey(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                ccls_data = DTMSRakeInwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_domestic_inward_rake(ccls_data,Constants.CGI_SURVEY_ENDPOINT)
                return result
            return {}
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                DTMSRakeInwardWriteService.update_VGI_survey(data,count)

