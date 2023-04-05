
from app.constants import GroundTruthType
from app.services.decorator_service import query_debugger
from app.services import soap_service
from app.services.rake.gt_upload_service import commit
from app.logger import logger
import app.constants as Constants
import config
import time
from datetime import datetime



class RakeInwardWriteService():
    def format_data_to_ccls_format(data):
        rake_data = {}
        if  Constants.KEY_TRAIN_NUMBER in data :
            rake_data[Constants.KEY_SOAP_TRAIN_NUMBER] = data[Constants.KEY_TRAIN_NUMBER]
        if Constants.KEY_DT_ACTUAL_DEPART in data:
            rake_data[Constants.KEY_SOAP_DT_ACTUAL_DEPART] = datetime.strptime(data[Constants.KEY_DT_ACTUAL_DEPART], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_IMP_EXP_FLG in data:
            rake_data[Constants.KEY_SOAP_IMP_EXP_FLG] = data[Constants.KEY_IMP_EXP_FLG]
        if Constants.KEY_FROM_LOC in data:
            rake_data[Constants.KEY_SOAP_FROM_LOC] = data[Constants.KEY_FROM_LOC]  
        if Constants.KEY_TO_LOC in data:
            rake_data[Constants.KEY_SOAP_TO_LOC] = data[Constants.KEY_TO_LOC]
        if Constants.KEY_TOTAL_WAGON_CONT in data:
            rake_data[Constants.KEY_SOAP_TOTAL_WAGON_CONT] = data[Constants.KEY_TOTAL_WAGON_CONT]
        if Constants.KEY_CURRENT_WAGON_COUNT in data:
            rake_data[Constants.KEY_SOAP_CURRENT_WAGON_COUNT] = data[Constants.KEY_CURRENT_WAGON_COUNT]
        if Constants.KEY_NO_LOADED_TEU_DEPART in data:
            rake_data[Constants.KEY_SOAP_NO_LOADED_TEU_DEPART] = data[Constants.KEY_NO_LOADED_TEU_DEPART]
        if Constants.KEY_NO_EMPTY_TEU_DEPART in data:
            rake_data[Constants.KEY_SOAP_NO_EMPTY_TEU_DEPART] = data[Constants.KEY_NO_EMPTY_TEU_DEPART]
        if Constants.KEY_NO_LOADED_TEU_ARRIVAL in data:
            rake_data[Constants.KEY_SOAP_NO_LOADED_TEU_ARRIVAL] = data[Constants.KEY_NO_LOADED_TEU_ARRIVAL]
        if Constants.KEY_NO_EMPTY_TEU_ARRIVAL in data:
            rake_data[Constants.KEY_SOAP_NO_EMPTY_TEU_ARRIVAL] = data[Constants.KEY_NO_EMPTY_TEU_ARRIVAL]    
        if Constants.KEY_CONTAINER_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_NUMBER] = data[Constants.KEY_CONTAINER_NUMBER]
        if Constants.KEY_CONTAINER_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_CONTAINER_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_SLINE_CODE in data:
            rake_data[Constants.KEY_SOAP_SLINE_CODE] = data[Constants.KEY_SLINE_CODE]
        if Constants.ISO_CODE in data:
            rake_data[Constants.KEY_SOAP_ISO_CODE] = data[Constants.ISO_CODE]
        if Constants.KEY_CONTAINER_SIZE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_SIZE] = data[Constants.KEY_CONTAINER_SIZE]
        if Constants.KEY_CONTAINER_TYPE in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_TYPE] = data[Constants.KEY_CONTAINER_TYPE]
        if Constants.KEY_CARGO_TYPE in data:
            rake_data[Constants.KEY_SOAP_CARGO_TYPE] = data[Constants.KEY_CARGO_TYPE]
        if Constants.KEY_LDD_MT_FLG in data:
            rake_data[Constants.KEY_SOAP_LDD_MT_FLG] = data[Constants.KEY_LDD_MT_FLG]
        if Constants.KEY_FCL_LCL_FLG in data:
            rake_data[Constants.KEY_SOAP_FCL_LCL_FLG] = data[Constants.KEY_FCL_LCL_FLG]
        if Constants.KEY_WAGON_NUMBER in data:
            rake_data[Constants.KEY_SOAP_WAGON_NUMBER] = data[Constants.KEY_WAGON_NUMBER]
        if Constants.KEY_WAGON_LIFE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_WAGON_LIFE_NUMBER] = datetime.strptime(data[Constants.KEY_WAGON_LIFE_NUMBER], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_WAGON_TYPE in data:
            rake_data[Constants.KEY_SOAP_WAGON_TYPE] = data[Constants.KEY_WAGON_TYPE]
        if Constants.KEY_DAMAGE_FLAG in data:
            rake_data[Constants.KEY_SOAP_DAMAGE_FLAG] = data[Constants.KEY_DAMAGE_FLAG]
        if Constants.KEY_PLACEMENT_REMARK in data:
            rake_data[Constants.KEY_SOAP_PLACEMENT_REMARK] = data[Constants.KEY_PLACEMENT_REMARK]
        if Constants.KEY_HLD_TRACK_NUMBER in data:
            rake_data[Constants.KEY_SOAP_HLD_TRACK_NUMBER] = data[Constants.KEY_HLD_TRACK_NUMBER]
        if Constants.KEY_GATEWAY_PORT_CD in data:
            rake_data[Constants.KEY_SOAP_GATEWAY_PORT_CD] = data[Constants.KEY_GATEWAY_PORT_CD]
        if Constants.KEY_SEAL_NUMBER in data:
            rake_data[Constants.KEY_SOAP_SEAL_NUMBER] = data[Constants.KEY_SEAL_NUMBER]
        if Constants.KEY_SEAL_STATUS in data:
            rake_data[Constants.KEY_SOAP_SEAL_STATUS] = data[Constants.KEY_SEAL_STATUS]
        if Constants.KEY_DAMAGE_CODE in data:
            rake_data[Constants.KEY_SOAP_DAMAGE_CODE] = data[Constants.KEY_DAMAGE_CODE]
        if Constants.KEY_HAZARD_STATUS in data:
            rake_data[Constants.KEY_SOAP_HAZARD_STATUS] = data[Constants.KEY_HAZARD_STATUS]
        if Constants.KEY_WAGON_DEST in data:
            rake_data[Constants.KEY_SOAP_WAGON_DEST] = data[Constants.KEY_WAGON_DEST]
        if Constants.KEY_DT_PLACEMENT in data:
            rake_data[Constants.KEY_SOAP_DT_PLACEMENT] = datetime.strptime(data[Constants.KEY_DT_PLACEMENT], '%Y-%m-%d %H:%M:%S')
        if Constants.KEY_EQUIPMENT_ID in data:
            rake_data[Constants.KEY_SOAP_EQUIPMENT_ID] = data[Constants.KEY_EQUIPMENT_ID]
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
    def update_track_for_container(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                ccls_data = RakeInwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_inward_rake(ccls_data,Constants.UPDATE_RAKE_CONTAINER_ENDPOINT)
                return result
            return {}
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeInwardWriteService.update_track_for_container(data,count)
    
    @query_debugger()
    def update_CGI_survey(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                ccls_data = RakeInwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_inward_rake(ccls_data,Constants.CGI_SURVEY_ENDPOINT)
                return result
            return {}
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeInwardWriteService.update_CGI_survey(data,count)
                
    @query_debugger()
    def update_inward_train_summary(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                request_data = RakeInwardWriteService.format_data_to_ccls_format(data)
                result = soap_service.update_inward_rake(request_data,Constants.UPDATE_INWARD_WTR_ENDPOINT)
                return result
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeInwardWriteService.update_inward_rake_details(data,count=count,isRetry=Constants.KEY_RETRY_VALUE)
                