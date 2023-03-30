from app.constants import GroundTruthType
from app.services.decorator_service import query_debugger
from app.services import soap_service
from app.services.gt_upload_service import commit
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
        if Constants.KEY_TRACK_NUMBER in data:
            rake_data[Constants.KEY_SOAP_HLD_TRACK_NUMBER] = data[Constants.KEY_TRACK_NUMBER]
        if Constants.KEY_WAGON_NUMBER in data:
            rake_data[Constants.KEY_SOAP_WAGON_NUMBER] = data[Constants.KEY_WAGON_NUMBER]
        if Constants.KEY_CONTAINER_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_NUMBER] = data[Constants.KEY_CONTAINER_NUMBER]
        if Constants.KEY_CONTAINER_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_CONTAINER_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S') 
        if Constants.KEY_CONTAINER_SIZE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_SIZE] = data[Constants.KEY_CONTAINER_SIZE]
        if Constants.KEY_CONTAINER_TYPE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_TYPE] = data[Constants.KEY_CONTAINER_TYPE]
        if Constants.KEY_CONTAINER_STAT in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_STAT] = data[Constants.KEY_CONTAINER_STAT]
        # Not supported in RakeOutWardWrite
        # if Constants.KEY_SEAL_NUMBER in data:
        #     rake_data[Constants.KEY_SOAP_SEAL_NUMBER] = data[Constants.KEY_SEAL_NUMBER]
        # if Constants.KEY_HAZARD_STATUS in data:
        #     rake_data[Constants.KEY_SOAP_HAZARD_STATUS] = data[Constants.KEY_HAZARD_STATUS]
        if Constants.KEY_DAMAGE_FLAG in data:
            rake_data[Constants.KEY_SOAP_DAMAGE_FLAG] = data[Constants.KEY_DAMAGE_FLAG]
        if "equipment_name" in data:
            rake_data[Constants.KEY_SOAP_EQUIPMENT_ID] = data["equipment_name"]
        if Constants.KEY_EQUIPMENT_ID in data:
            rake_data[Constants.KEY_SOAP_EQUIPMENT_ID] = data[Constants.KEY_EQUIPMENT_ID]
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