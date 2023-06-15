from app.services.decorator_service import query_debugger
from app.models import RakePlan
from app import db
from app.constants import GroundTruthType
import app.constants as Constants
from app.services import soap_service
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE
from datetime import datetime,timedelta
import config
import json
import time

class RakeOutwardPlanService():
    @query_debugger()
    def add_rake_plan(rake_data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                    pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            try:
                print(type(rake_data))
                containers =  rake_data.pop("containers")
                for each in containers:
                    each.update(rake_data)
                    rake_plan_container = RakePlan(**each)
                    db.session.add(rake_plan_container)
                return commit()
            except Exception as e:
                logger.exception(str(e))
                return False
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeOutwardPlanService.add_rake_plan(rake_data,count)
                
    @query_debugger()
    def get_rake_plan(rake_id,train_number=None,track_number=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                    pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            
            rake_query = RakePlan.query.filter_by(rake_id=rake_id)
            update_data = {}
            if track_number:
                update_data['hld_track_number'] = track_number
            if train_number :
                update_data['train_number'] = train_number
            if update_data:
                rake_query.update(dict(update_data))
                commit()
                logger.info("updated db")
            data = rake_query.all()
            return RakeOutwardPlanService.format_rake_plan(data)
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeOutwardPlanService.get_rake_plan(rake_id,train_number,track_number,count)
    
    def format_rake_plan(data):
        response = {}
        if len(data)>0:
            response[Constants.RAKE_ID] = data[0].rake_id
            response[Constants.TRACK_NUMBER] = data[0].hld_track_number
            response[Constants.RAKE_NUMBER]  = data[0].rake_number
            response[Constants.TRAIN_NUMBER]  = data[0].train_number
            response[Constants.RAKE_TYPE] = data[0].attribute_1
            response[Constants.WAGON_LIST] = []
            response[Constants.CONTAINER_LIST] = []
            for i in range(len(data)):
                wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].attribute_4}}
                response[Constants.WAGON_LIST].append(wagon_record)
                container_record ={}
                container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i].container_number}
                container_record[Constants.KEY_CONTAINER_LIFE_NUMBER] = data[i].container_life_number
                container_record[Constants.COMMIDITY]= data[i].attribute_2
                container_record[Constants.LINER_SEAL] = {Constants.VALUE : data[i].attribute_3}
                container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i].attribute_3}
                container_record[Constants.POD] = data[i].first_pod
                container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i].iso_code if data[i].iso_code else str(data[i].container_size)+str(data[i].container_type) if data[i].container_size and data[i].container_type else None}
                container_record[Constants.LDD_MT_FLAG] = {Constants.VALUE : data[i].ldd_mt_flg} 
                container_record[Constants.KEY_SLINE_CODE] =  {Constants.VALUE : data[i].sline_code}
                container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].attribute_4}
                response[Constants.CONTAINER_LIST].append(container_record)
        return json.dumps(response)