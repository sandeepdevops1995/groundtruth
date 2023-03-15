import app.constants as Constants
import config
import json
from app.logger import logger
from sqlalchemy.sql import text
from sqlalchemy import cast, DATE
from app import engine as e
import os
from app.services.decorator_service import query_debugger
from app.logger import logger
import time;
from sqlalchemy.exc import SQLAlchemyError
from app.constants import GroundTruthType
from app.models import CCLSRake
from app.services import soap_service
from app.services.gt_upload_service import commit
from app.models import *
from datetime import datetime,timedelta


class RakeDbService:

    @query_debugger()
    def get_rake_details_by_rake_number(rake_number,rake_type="AR",from_date=None,to_date=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                if(rake_type=="DE"):
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_out_details_by_rake_number.sql"))
                else:
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_in_details_by_rake_number.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command,rake_number=rake_number)
                sqlFile.close()
                conn.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                return RakeDbService.map_CCLS_response(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
               pass
            data = CCLSRake.query.filter_by(rake_number=rake_number).all()
            return RakeDbService.format_rake_data(data)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_rake_details_by_rake_number(rake_number,rake_type,from_date,to_date,count,isRetry)
                
    @query_debugger()
    def get_track_details(query_values,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            if "trans_date" in query_values:
                data = Track.query.filter(cast(Track.trans_date, DATE)==query_values["trans_date"])
                query_values.pop('trans_date')
                data = data.filter_by(**query_values).order_by('trans_date').all()
            else:
                data = Track.query.filter_by(**query_values).all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_track_details(query_values,count,isRetry)
                
    @query_debugger()
    def post_track_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            if isinstance(data, list):
                for item in data:
                    track =Track(**item)
                    db.session.add(track)
            else:
                track = Track(**data)
                db.session.add(track)
            try:   
                commit()
                return True,"success"
            except Exception as e:
                print(e)
                return False,str(e)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.post_track_details(data,count,isRetry)
    
    @query_debugger()
    def get_train_details(query_values,rake_id=None,track_number=None,from_date=None,to_date=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                result = {}
                if from_date and to_date:
                    result = soap_service.get_train_data(from_date=from_date,to_date=to_date)
                    if result:
                        data = RakeDbService.save_in_db(result)
                        return RakeDbService.format_rake_data(data)                        
                    return []
                # elif "train_number" in query_values["train_number"]:
                #     result = soap_service.get_train_data(query_values["train_number"])
            if "trans_date" in query_values:
                trans_date = query_values.pop('trans_date')
                start_date = trans_date - timedelta(days = 2)
                end_date =  trans_date + timedelta(days = 2)
                rake_query = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)>=start_date, cast(CCLSRake.trans_date, DATE)<=end_date)
                rake_query = rake_query.filter_by(**query_values)
            else:
                rake_query = CCLSRake.query.filter_by(**query_values)
            update_data = {}
            if track_number:
                update_data['track_number'] = track_number
            if rake_id :
                update_data['rake_id'] = rake_id
            rake_query.update(dict(update_data))
            commit()
            data = rake_query.order_by('trans_date').all()
            return RakeDbService.format_rake_data(data)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_train_details(query_values,track_number,from_date,to_date,count,isRetry)

    def save_in_db(data_list):
        final_data = []
        for each in data_list:
            wagon = {}
            wagon["container_number"] = each["ctrNo"][0]
            wagon["container_life_number"] = each["ctrLifeNo"][0]
            wagon["sline_code"] = each["slineCd"][0]
            wagon["iso_code"] = each["ctrIsoCd"][0]
            wagon["container_size"] = each["ctrSize"][0]
            wagon["container_type"] = each["ctrType"][0]
            wagon["cargo_type"] = each["crgType"][0]
            wagon["ldd_mt_flg"] = each["lddMtFlg"][0]
            wagon["fcl_lcl_flg"] = each["fclLclFlg"][0]
            wagon["station_cd"] = each["stnCd"][0]
            wagon["train_number"] = each["trnNo"][0]
            wagon["wagon_number"] = each["wgnNo"][0]
            wagon["wagon_type"] = each["wgnType"][0]
            wagon["gw_port_cd"] = each["gwPortCd"][0]
            wagon["container_stg_flag"] = each["ctrStgFlg"][0]
            wagon["error_flg"] = each["errFlg"][0]
            wagon["container_iwb_flag"] = each["ctrIwbFlg"][0]
            wagon["remark"] = each["rmrk"][0]
            wagon["cancel_flg"] = each["cnclFlg"][0]
            wagon["trans_date"] = each["trnsDtTm"][0]
            wagon["user_id"] = each["userId"][0]
            wagon["wagon_life_number"] = each["wgnLifeNo"][0]
            wagon["smtp_no"] = each["smtpNo"][0]
            wagon["smtp_date"] = each["smtpDt"][0]
            wagon["container_gross_weight"] = each["ctrWt"][0]
            wagon["port_name"] = each["portNam"][0]
            wagon["train_dept"] = each["trnDep"][0]
            
            query_fields = {"wagon_number" : wagon["wagon_number"],
             "container_number" : wagon["container_number"],
            # "container_life_number" : wagon["container_life_number"],
            "trans_date" : wagon["trans_date"],
            "train_number" : wagon["train_number"]}
            wagon_model = CCLSRake(**wagon)
            final_data.append(wagon_model)
            try:
                result = CCLSRake.query.filter_by(**query_fields)
                if result.all():
                    result.update(dict(wagon))
                    logger.info("Updated existing wagon")
                else:
                    db.session.add(wagon)
                commit()
            except Exception as e:
                logger.exception(str(e))
        
        return final_data

    def format_rake_data(data):
        response = {}
        if len(data)>0:
            response[Constants.RAKE_ID] = data[0].rake_id
            response[Constants.TRACK_NUMBER] = data[0].track_number
            response[Constants.RAKE_NUMBER]  = data[0].rake_number
            response[Constants.TRAIN_NUMBER]  = data[0].train_number
            response[Constants.RAKE_TYPE] = data[0].rake_type
            response[Constants.WAGON_LIST] = []
            response[Constants.CONTAINER_LIST] = []
            for i in range(len(data)):
                wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].wagon_sequence_number}}
                response[Constants.WAGON_LIST].append(wagon_record)
                container_record ={}
                container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i].container_number}
                container_record[Constants.COMMIDITY]= data[i].attribute_2
                container_record[Constants.LINER_SEAL] = {Constants.VALUE : data[i].attribute_3}
                container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i].seal_number}
                container_record[Constants.POD] = data[i].container_destination_station
                container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i].iso_code if data[i].iso_code else str(data[i].container_size)+str(data[i].container_type) if data[i].container_size and data[i].container_type else None}
                container_record[Constants.LDD_MT_FLAG] = {Constants.VALUE : data[i].ldd_mt_flg} 
                container_record[Constants.KEY_SLINE_CODE] =  {Constants.VALUE : data[i].sline_code}
                container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].wagon_sequence_number}
                response[Constants.CONTAINER_LIST].append(container_record)
        return json.dumps(response)
    
    @query_debugger()
    def get_rake_details_by_track_number(track_number,rake_type="AR",count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                if(rake_type=="DE"):
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_out_details_by_track_number.sql"))
                else:
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_in_details_by_track_number.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command,track_number=track_number)
                sqlFile.close()
                conn.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                return RakeDbService.map_CCLS_response(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                track = Track.query.filter_by(track_no=track_number).first()
                if track:
                    if track.train_no and track.trans_date:
                        query_values = {"train_number":track.train_no, "trans_date":track.trans_date.date()}
                        return True, RakeDbService.get_train_details(query_values)
                    else: 
                        return False, "No train available in the given track"
                else:
                    return False, "No such Track Exists"
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_rake_details_by_track_number(track_number,rake_type,count=count,isRetry=Constants.KEY_RETRY_VALUE)


    def get_container_data(container_number):
        if config.GROUND_TRUTH == GroundTruthType.SOAP.value:
            pass
        data = CCLSRake.query.filter_by(container_number=container_number).all()
        if data:
            return RakeDbService.format_rake_data(data)
        else:
            return {}
        
        
    @query_debugger()
    def update_inward_rake_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                request_data = RakeDbService.get_soap_format_for_rake(data)
                result = soap_service.update_inward_rake(request_data)
                return result
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.update_inward_rake_details(data,count=count,isRetry=Constants.KEY_RETRY_VALUE)
                    
    
    @query_debugger()
    def update_outward_rake_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                request_data = RakeDbService.get_soap_format_for_rake(data)
                result = soap_service.update_outward_rake(request_data)
                return result
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.update_outward_rake_details(count=count,isRetry=Constants.KEY_RETRY_VALUE)

    
    def get_soap_format_for_rake(data):
        rake_data = {}
        if  Constants.KEY_TRAIN_NUMBER in data :
            rake_data[Constants.KEY_SOAP_TRAIN_NUMBER] = data[Constants.KEY_TRAIN_NUMBER]
        if Constants.KEY_IMP_EXP_FLG in data:
            rake_data[Constants.KEY_SOAP_IMP_EXP_FLG] = data[Constants.KEY_IMP_EXP_FLG]
        if Constants.KEY_DT_ACTUAL_DEPART in data:
            rake_data[Constants.KEY_SOAP_DT_ACTUAL_DEPART] = data[Constants.KEY_DT_ACTUAL_DEPART]
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
            rake_data[Constants.KEY_SOAP_CONTAINER_LIFE_NUMBER] = data[Constants.KEY_CONTAINER_LIFE_NUMBER]
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
            rake_data[Constants.KEY_SOAP_WAGON_LIFE_NUMBER] = data[Constants.KEY_WAGON_LIFE_NUMBER]
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
        if Constants.KEY_HAZARD_STATUS in data:
            rake_data[Constants.KEY_SOAP_HAZARD_STATUS] = data[Constants.KEY_HAZARD_STATUS]
        if Constants.KEY_WAGON_DEST in data:
            rake_data[Constants.KEY_SOAP_WAGON_DEST] = data[Constants.KEY_WAGON_DEST]
        if Constants.KEY_DT_PLACEMENT in data:
            rake_data[Constants.KEY_SOAP_DT_PLACEMENT] = data[Constants.KEY_DT_PLACEMENT]
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
            rake_data[Constants.KEY_SOAP_ATTRIBUTE6] = data[Constants.KEY_ATTRIBUTE6]
        if Constants.KEY_ATTRIBUTE7 in data:
            rake_data[Constants.KEY_SOAP_ATTRIBUTE7] = data[Constants.KEY_ATTRIBUTE7]
        if Constants.KEY_CREATED_AT in data:
            rake_data[Constants.KEY_SOAP_CREATED_AT] = data[Constants.KEY_CREATED_AT]
        if Constants.KEY_CREATED_BY in data:
            rake_data[Constants.KEY_SOAP_CREATED_BY] = data[Constants.KEY_CREATED_BY]
        if Constants.KEY_UPDATED_AT in data:
            rake_data[Constants.KEY_SOAP_UPDATED_AT] = data[Constants.KEY_UPDATED_AT]
        if Constants.KEY_UPDATED_BY in data:
            rake_data[Constants.KEY_SOAP_UPDATED_BY] = data[Constants.KEY_UPDATED_BY]
        if Constants.KEY_ERROR_MSG in data:
            rake_data[Constants.KEY_SOAP_ERROR_MSG] = data[Constants.KEY_ERROR_MSG]
        if Constants.KEY_STATUS_FLG in data:
            rake_data[Constants.KEY_SOAP_STATUS_FLG] = data[Constants.KEY_STATUS_FLG]
        if Constants.KEY_READ_FLG in data:
            rake_data[Constants.KEY_SOAP_READ_FLG] = data[Constants.KEY_READ_FLG]
        if Constants.KEY_DT_DESP in data:
            rake_data[Constants.KEY_SOAP_DT_DESP] = data[Constants.KEY_DT_DESP]
        if Constants.KEY_RAKE_NUMBER in data:
            rake_data[Constants.KEY_SOAP_RAKE_NUMBER] = data[Constants.KEY_RAKE_NUMBER]
        if Constants.KEY_DT_WTR in data:
            rake_data[Constants.KEY_SOAP_DT_WTR] = data[Constants.KEY_DT_WTR]
        if Constants.KEY_CONTAINER_WEIGHT in data:
            rake_data[Constants.KEY_SOAP_CONTAINER_WEIGHT] = data[Constants.KEY_CONTAINER_WEIGHT]
        if Constants.KEY_FIRST_POD in data:
            rake_data[Constants.KEY_SOAP_FIRST_POD] = data[Constants.KEY_FIRST_POD]
        if Constants.KEY_ORIGIN_STATION in data:
            rake_data[Constants.KEY_SOAP_ORIGIN_STATION] = data[Constants.KEY_ORIGIN_STATION]
        if Constants.KEY_DEST_STATION in data:
            rake_data[Constants.KEY_SOAP_DEST_STATION] = data[Constants.KEY_DEST_STATION]
        return rake_data

    @query_debugger()
    def get_ground_truth_details(train_number, trans_date, count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):

        trans_date = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S').date()
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            
            data = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)==trans_date).filter_by(train_number=train_number).all()
            if data:
                return db_functions(data).as_json()
            else:
                return json.dumps({})
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_ground_truth_details(train_number, trans_date, count=count,isRetry=Constants.KEY_RETRY_VALUE)

    @query_debugger()
    def post_ground_truth_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            for each in data:
                if "id" in each:
                        each.pop("id")
                result = CCLSRake.query.filter_by(train_number = each['train_number'],wagon_number= each['wagon_number'],container_number= each['container_number'],container_life_number= each['container_life_number']).all()
                if not result:
                    wagon = CCLSRake(**each)
                    db.session.add(wagon)
                else:
                    print(each["train_number"],each["wagon_number"],each["container_number"])
                    logger.info("corresponding train, wagon and container exists in given trans_date")
            try:
                commit()
                return True,"Saved Successfully"
            except Exception as e:
                logger.exception(str(e))
                return False,str(e)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.post_ground_truth_details(data,count=count,isRetry=Constants.KEY_RETRY_VALUE)


    @query_debugger()
    def get_pendancy_list(gateway_ports,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = PendancyContainer.query.filter(PendancyContainer.gateway_port_code.in_(gateway_ports)).order_by(PendancyContainer.gateway_port_code).all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_pendancy_list(data,count=count,isRetry=Constants.KEY_RETRY_VALUE)

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
                RakeDbService.add_rake_plan(rake_data,count)
                
    @query_debugger()
    def get_rake_plan(rake_id,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                    pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = RakePlan.query.filter_by(rake_id=rake_id).all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeDbService.get_rake_plan(rake_id,count)
    
    
    @query_debugger()
    def add_wagon_to_master_data(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            try:
                for each in data:
                    wagon = WgnMst(**each)
                    db.session.add(wagon)
                return commit()
            except Exception as e:
                logger.exception(str(e))
                return False
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeDbService.add_wagon_to_master_data(data,count)
        
    
    @query_debugger()
    def get_wagon_master_data(wagon_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = WgnMst.query.filter(WgnMst.wgn_no.contains(wagon_number),WgnMst.active_flg=='Y').all()
            return data
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeDbService.get_wagon_master_data(wagon_number,count)

    @query_debugger()
    def add_gateway_port_to_master_data(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            try:
                for each in data:
                    port = Gwport(**each)
                    db.session.add(port)
                return commit()
            except Exception as e:
                logger.exception(str(e))
                return False
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeDbService.add_wagon_to_master_data(data,count)
        
    
    @query_debugger()
    def get_gateway_port_master_data(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Gwport.query.all()
            return data
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                RakeDbService.get_wagon_master_data(count)          

    @query_debugger()
    def get_wagon_data(wagon_number,rake_type="DE",count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                if(rake_type=="DE"):
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_out_details_by_wagon_number.sql"))
                else:
                    sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_in_details_by_wagon_number.sql"))
                # sqlFile = open(os.path.join(config.SQL_DIR,"get_rake_out_details_by_wagon_number.sql"))

                command = text(sqlFile.read())
                query = conn.execute(command,wagon_number=wagon_number)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return RakeDbService.map_CCLS_response(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CCLSRake.query.filter_by(wagon_number=wagon_number).all()
            if data:
                return RakeDbService.format_rake_data(data)
            else:
                return {}
        except SQLAlchemyError as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_wagon_data(wagon_number,rake_type,count,isRetry)

    def update_rake_wagon_data(data,wagon_number=None):
        response = data.copy()
        response[Constants.WAGON_LIST] =[]
        response[Constants.CONTAINER_LIST] =[]
        for each in data[Constants.WAGON_LIST]:
            if each[Constants.WAGON_NUMBER][Constants.NUMBER] == wagon_number:
                response[Constants.WAGON_LIST].append(each)
        for each in data[Constants.CONTAINER_LIST]:
            if Constants.WAGON_NUMBER in each and each[Constants.WAGON_NUMBER][Constants.NUMBER] == wagon_number:
                response[Constants.CONTAINER_LIST].append(each)
        return response

    def get_rake_details(rake_number=None, track_number=None,rake_type=None):
        result = None
        if track_number:
            result = RakeDbService.get_rake_details_by_track_number(track_number=track_number,rake_type=rake_type)
        elif rake_number:
            result = RakeDbService.get_rake_details_by_rake_number(rake_number=rake_number,rake_type=rake_type)
        return result


    def update_rake_json_format(self,rake_data):
        updated_data ={}
        rake_numbers =set([cnt_record[config.RAKE_NUMBER] for cnt_record in rake_data ])
        for rake_number in rake_numbers:
            updated_data[rake_number] =[]
            [updated_data[rake_number].append(record) for record in rake_data if rake_number == record[config.RAKE_NUMBER]]
        return updated_data


    @query_debugger()
    def update_inward_wtr_train_summ(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                #upadate WTR
                sqlFile = open(os.path.join(config.SQL_DIR,"insert_inward_wtr_details.sql"))
                command = text(sqlFile.read())
                wtr_no = 121528
                wagons_list = data.get("wagon_list")
                for wagon in wagons_list:
                    wgn_no = wagon.get("wgn_no")
                    continers_list = wagon.get("ctr_list")
                    for container in continers_list:
                        ctr_no = container.get("ctr_no")
                        ctr_size = int(container.get("size"))
                        ctr_type = container.get("ctr_type")
                        seal_no = container.get("seal_no")
                        iso_code = container.get("iso_code")
                        sline_code = container.get("sline_code")
                        try:
                            query = conn.execute(command,wtr_no=wtr_no,wagon_number=wgn_no,container_number=ctr_no, container_size=ctr_size,
                            container_type=ctr_type,seal_number= seal_no,iso_code=iso_code,sline_code=sline_code)
                        except:
                            sqlFile.close()
                            conn.close()
                sqlFile.close()
                #update train Summary
                sqlFile = open(os.path.join(config.SQL_DIR,"insert_inward_train_summary.sql"))
                command = text(sqlFile.read())
                track_no = data.get("hld_track_no")
                wagon_count = int(data.get("Total_wgn_cnt"))
                try:
                    query = conn.execute(command,wtr_no= wtr_no,track_number=track_no,wagon_count=wagon_count)
                finally:
                    sqlFile.close()
                    conn.close()
                return        
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.update_inward_wtr_train_summ(count,isRetry)

    @query_debugger()
    def update_outward_wtr_train_summ(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                #upadate WTR
                sqlFile = open(os.path.join(config.SQL_DIR,"insert_outward_wtr_details.sql"))
                command = text(sqlFile.read())
                wtr_no = 121528
                wagons_list = data.get("wagon_list")
                for wagon in wagons_list:
                    wgn_no = wagon.get("wgn_no")
                    continers_list = wagon.get("ctr_list")
                    for container in continers_list:
                        ctr_no = container.get("ctr_no")
                        ctr_size = int(container.get("size"))
                        ctr_type = container.get("ctr_type")
                        seal_no = container.get("seal_no")
                        iso_code = container.get("iso_code")
                        sline_code = container.get("sline_code")
                        try:
                            query = conn.execute(command,wtr_no=wtr_no,wagon_number=wgn_no,container_number=ctr_no, container_size=ctr_size,
                            container_type=ctr_type,seal_number= seal_no,iso_code=iso_code,sline_code=sline_code)
                        except:
                            sqlFile.close()
                            conn.close()
                sqlFile.close()
                #update train Summary
                sqlFile = open(os.path.join(config.SQL_DIR,"insert_outward_train_summary.sql"))
                command = text(sqlFile.read())
                track_no = data.get("hld_track_no")
                wagon_count = int(data.get("Total_wgn_cnt"))
                try:
                    query = conn.execute(command,wtr_no= wtr_no,track_number=track_no,wagon_count=wagon_count)
                finally:
                    sqlFile.close()
                    conn.close()
                return        
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.update_outward_wtr_train_summ(count,isRetry)

    def map_CCLS_response(data):
        response = {}
        if len(data)>0:
            response[Constants.TRACK_NUMBER] = data[0]["track_number"]
            response[Constants.RAKE_NUMBER]  = data[0]["rake_number"]
            response[Constants.RAKE_TYPE] = data[0]["rake_type"]
            response[Constants.WAGON_LIST] = []
            response[Constants.CONTAINER_LIST] = []
            for i in range(len(data)):
                wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : data[i]["wagon_number"],Constants.KEY_ID:data[i]["wagon_id"]}}
                response[Constants.WAGON_LIST].append(wagon_record)
                container_record ={}
                container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i]["container_no"]}
                container_record[Constants.COMMIDITY]= data[i]["cargo_type"]
                container_record[Constants.LINER_SEAL] = {Constants.VALUE : data[i]["liner_seal"]}
                container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i]["custom_seal"]}
                container_record[Constants.POD] = data[i]["pod"]
                container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i]["iso_code"]}
                container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : data[i]["wagon_number"],Constants.KEY_ID:data[i]["wagon_id"]}
                response[Constants.CONTAINER_LIST].append(container_record)
            return json.dumps(response)    
        return data

    @query_debugger()
    def get_wagon_types(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_wagon_types.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = WgnType.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_wagon_types(count,isRetry)

    @query_debugger()
    def get_sline_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_sline_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = SlineConv.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_sline_codes(count,isRetry)

    @query_debugger()
    def get_icd_locations(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_icd_locations.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = IcdLoc.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_icd_locations(count,isRetry)

    @query_debugger()
    def get_pod_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_pod_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = PodConv.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_wget_pod_codesagon_types(count,isRetry)

    @query_debugger()
    def get_container_types(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_container_types.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CtrType.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_container_types(count,isRetry)

    @query_debugger()
    def get_commodity_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_commodity_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Commodity.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_commodity_codes(count,isRetry)

    @query_debugger()
    def get_commodity_types(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_commodity_types.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Comm.query.all()
            return db_functions(data).as_json()
            
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_commodity_types(count,isRetry)

    @query_debugger()
    def get_activity_types(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_activity_types.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Acty.query.all()
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_activity_types(count,isRetry)

    @query_debugger()
    def get_port_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_port_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Port.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_port_codes(count,isRetry)
    
    @query_debugger()
    def get_out_location_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_out_location_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = OutLoc.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_out_location_codes(count,isRetry)
    
    @query_debugger()
    def get_out_port_codes(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_out_port_codes.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = OutPort.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_out_port_codes(count,isRetry)
    
    @query_debugger()
    def get_cargo_types(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_cargo_types.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_cargo_types(count,isRetry)
    
    @query_debugger()
    def get_user_list(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                sqlFile = open(os.path.join(config.SQL_DIR,"get_user_list.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command)
                sqlFile.close()
                data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
                conn.close()
                return  json.dumps(data)
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = UserDtls.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_user_list(count,isRetry)


    def push_test_data_arrival():
        if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
            data=[[ "61250313395" , 1 , "BAXU5047981"],[ "62250319462" , 2 , "KMTU9346374" ],["62250320093" , 3 , "CAXU8112166" ],[ "62250320109" , 4 , "FCIU2645349" ],
            [ "61250313401" , 5 , "MRKU8647511" ],[ "61259900916" , 6 , "MRKU9888030" ], [ "62259901361" , 7 , "CSNU6388059" ],[ "62259901378" , 8 , "TTNU9934059" ],
            [ "62259901385" , 9 , 'TCLU7810927' ],[ "61259900923" , 10 , "TEMU3806206" ], [ "61250723583" , 11 , "SEGU4786854" ],[ "62250735378" , 12 , "TCNU8687671" ],
            [ "62250735361" , 13 , "TEMU7561159" ],[ "62250735354" , 14 , "TRHU3998925" ], [ "61250723576" , 15 , "MSKU5429842" ],[ "61250920555" , 16 , "TCLU2372875" ],
            [ "62250930827" , 17 , "HLXU1362650" ],[ "62250930834" , 18 , "MEDU6162850" ], [ '62250930841' , 19 , "TGHU0936980" ],[ "61250920562" , 20 , "ZCSU8515640" ],
            [ "61250725914" , 21 , "XXXU5855654" ],[ "62250738867" , 22 , "DRYU9457990" ], [ "62250738874" , 23 , "TLLU5970272" ],[ "62250738881" , 24 , "TCNU4877204" ],
            [ "61250725921" , 25 , "XXXU5967511" ],[ "61250460082" , 26 , "HLXU1030526" ], [ "62250460119" , 27 , "MRKU8464038" ],[ "62250460102" , 28 , "CMAU0168107" ],
            [ "62250460096" , 29 , "TCLU5746496" ],[ '61250460075' , 30 , "TCNU5466430" ], [ "61250621179" , 31 , "CLSU4000365" ],[ "62250631755" , 32 , "BMOU6172713" ],
            [ '62250631762' , 33 , "MRSU0177590" ],[ "62250631779" , 34 , "CSQU3045381"], [ '61250621186' , 35 , "KOCU4736064" ],[ '61251544569' , 36 , "TGHU3967265" ],
            [ "62251566797" , 37 , "CAIU8751967" ],[ '62251566780' , 38 , "TCNU6434592" ], [ "62251566773" , 39 , "CAXU8027974" ],[ "61251544552" , 40 , "TCNU1895734" ],
            [ "61250516536" , 41 , "MRSU4052098" ],[ "62250524798" , 42 , "UACU3903717" ], [ "62250524804" , 43 , "FCIU7109544" ],[ "62250524811" , 44 , "MEDU4683757" ],
            [ "61250516543" , 45 , "NYKU0784920" ]]
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"insert_data_tt-cinadvctr.sql"))
            command = text(sqlFile.read())
            for i in range(len(data)):
                conn.execute(command,container_number=data[i][2],wagon_number=data[i][0],wagon_id=data[i][1])
            sqlFile.close()

            sqlFile = open(os.path.join(config.SQL_DIR,"insert_data_tt-cinadvchk.sql"))
            command = text(sqlFile.read())
            for i in range(len(data)):
                conn.execute(command,container_number=data[i][2],wagon_number=data[i][0])
            sqlFile.close()
            conn.close()
            return

    def push_test_data_departure():
        if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
            data= [[ "61251340109" , 1 , "TEMU8400729" ],[ "62251360159" , 2 , "FCIU7273579" ],
            [ "62251360142" , 3 , "MRKU7273579" ],[ "62251360135" , 4 , "ZESU7273579" ],
            [ "61251340093" , 5 , "TCKU7273579" ]]
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"insert_data_tt-coutadvctr-rake.sql"))
            command = text(sqlFile.read())
            for i in range(len(data)):
                conn.execute(command,container_number=data[i][2],wagon_number=data[i][0])
            sqlFile.close()
            return
        
    def get_rake_file_data(self,file_obj):
        import pandas as pd
        try:
            dframe = pd.read_excel(file_obj, engine='openpyxl')
            data = dframe.to_json(orient = "records" )
            j_data = json.loads(data)
            return j_data
        except Exception as e:
            logger.error('file format or data is missing', e)
            j_data=[]
            return j_data
    
    def save_rake_details(self,data):
        for each in data:
            wagon=CCLSRake(**each)
            try:
                result = CCLSRake.query.filter_by(train_number=each["train_number"],
                                                  wagon_number=each["wagon_number"],
                                                  container_number=each["container_number"])
                if result.all():
                    result.update(dict(each))
                    logger.info("Updated existing wagon")
                else:
                    db.session.add(wagon)
                commit()
            except Exception as e:
                logger.exception(str(e))
                    

def get_iso_by_type_and_size(container_type, container_size):
    iso_code="22G1"
    try:
        iso_code = Constants.CONTAINER_LENGTH_ISO_MAPPING[str(int(container_size))] + \
            Constants.CONTAINER_TYPE_ISO_MAPPING[str(container_type)]
    except Exception as e:
        logger.error(repr(e), exc_info=True)
    return iso_code


def Rake_Key_Mapping(rake_details,rake_number):
    rake_data = {}
    wagon_list = []
    container_list = []
    container_record ={}
    record = {}
    if(config.TRACK_NUMBER in rake_details[0].keys()):
        record[Constants.TRACK_NUMBER] = str(rake_details[0][config.TRACK_NUMBER])

    if(config.RAKE_NUMBER in rake_details[0].keys()):
        record[Constants.RAKE_NUMBER] = rake_number

    record[Constants.RAKE_TYPE] = rake_details[0][config.RAKE_TYPE]

    added_list=[]
    for each in rake_details:
        if each[config.WAGON_NUMBER]:
            wagon_number = int(each[config.WAGON_NUMBER])
            if wagon_number  in added_list:
                continue
            added_list.append(wagon_number)
            wagon_list.append({Constants.WAGON_NUMBER :{ Constants.NUMBER : wagon_number,Constants.KEY_ID:len(added_list)}})



    record[Constants.WAGON_LIST] = wagon_list
    for each in rake_details:
        if each[config.CONTAINER_NUM] and each[config.CONTAINER_NUM] != "":
            container_record ={}
            container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : each[config.CONTAINER_NUM]}
            container_record[Constants.COMMIDITY]= each[config.COMMIDITY]
            container_record[Constants.LINER_SEAL] = {Constants.VALUE : each[config.R_LINER_SEAL]}
            container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : each[config.R_CUSTOM_SEAL]}
            container_record[Constants.POD] = each[config.DESTINATION_STATION]
            container_record[Constants.UN_NUMBER] = json.loads(each[config.UN_NUMBER]) if isinstance(each[config.UN_NUMBER],str) and each[config.UN_NUMBER]!=None else each[config.UN_NUMBER] if each[config.UN_NUMBER]!=None else []
            container_record[Constants.HAZARD] = json.loads(each[config.HAZARD]) if isinstance(each[config.HAZARD],str) and each[config.HAZARD]!=None else each[config.HAZARD] if each[config.HAZARD]!=None else []
            container_record[Constants.ISO_CODE] = {Constants.VALUE : get_iso_by_type_and_size(each[config.CONTAINER_TYPE],each[config.CONTAINER_SIZE])}

            # if(record[Constants.RAKE_TYPE] == Constants.ARRIVAL):
            w_num = int(each[config.WAGON_NUMBER])
            container_record[Constants.WAGON_NUMBER] = [each[Constants.WAGON_NUMBER] for each in wagon_list if each[Constants.WAGON_NUMBER][Constants.NUMBER] == w_num][0]

            container_list.append(container_record)

    record[Constants.CONTAINER_LIST] = container_list
    return  record
