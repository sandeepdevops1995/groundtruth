from app.services.decorator_service import query_debugger
from app.models import CCLSRake, WgnMst, MissedInwardContainers
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


class RakeInwardReadService:

    @query_debugger()
    def get_train_details(query_values,rake_id=None,track_number=None,trans_delay=2,from_date=None,to_date=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                result = {}
                if from_date and to_date:
                    result = soap_service.get_exim_train_details(from_date=from_date,to_date=to_date)
                    if result:
                        data = RakeInwardReadService.save_in_db(result)
                        return RakeInwardReadService.format_rake_data(data)                        
                    return []
                # elif "train_number" in query_values["train_number"]:
                #     result = soap_service.get_exim_train_details(query_values["train_number"])
            if "trans_date" in query_values:
                trans_date = query_values.pop('trans_date')
                start_date = trans_date - timedelta(days = trans_delay)
                end_date =  trans_date + timedelta(days = trans_delay)
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
            data = rake_query.order_by(desc('trans_date')).all()
            if 'rake_id' in query_values:
                missed_containers = MissedInwardContainers.query.filter_by(rake_id=query_values['rake_id']).all()
                data = data + missed_containers
            if not data and "train_number" in query_values:
                logger.info("fetch train details from soap service for train number "+query_values['train_number'])
                result = soap_service.get_exim_train_details(train_number=query_values['train_number'])
                if result:
                    logger.info("Data exists in Soap Servcie for given train number "+query_values['train_number'])
                    data = RakeInwardReadService.save_in_db(result)
            return RakeInwardReadService.format_rake_data(data)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeInwardReadService.get_train_details(query_values,rake_id,track_number,trans_delay,from_date,to_date,count,isRetry)

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
            if "SEAL_NO" in each:
                wagon["seal_number"] = each["SEAL_NO"][0 ]
            
            query_fields = {"wagon_number" : wagon["wagon_number"],
             "container_number" : wagon["container_number"],
            # "container_life_number" : wagon["container_life_number"],
            "trans_date" : wagon["trans_date"],
            "train_number" : wagon["train_number"]}
            
            # save in CCLSRake
            wagon_model = CCLSRake(**wagon)
            final_data.append(wagon_model)
            try:
                result = CCLSRake.query.filter_by(**query_fields)
                if result.all():
                    result.update(dict(wagon))
                    logger.info("Updated existing wagon")
                else:
                    db.session.add(wagon_model)
                commit()
            except Exception as e:
                logger.exception(str(e))
            
            # Save in Wagon Master
            wagon_data = {"wgn_no" : wagon["wagon_number"]}
            try:
                wagon = WgnMst.query.filter_by(**wagon_data).all()
                if not wagon:
                    wagon_data["wgn_typ"] = "BLCB"
                    wagon_data["commisioned_on"] = datetime.now()
                    wagon = WgnMst(**wagon_data)
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
                # container_record[Constants.CONTAINER_STAT] = "L" if "container_gross_weight" in data[i] and data[i].container_gross_weight else "E"
                container_record[Constants.CONTAINER_STAT] = "E"
                # category: "Import/Export/Domestic/Transhipment"
                container_record[Constants.CATEGORY] = "Import"

                response[Constants.CONTAINER_LIST].append(container_record)
        return json.dumps(response)
    

    def format_cmts_data(data):
        response = []
        for i in range(len(data)):
            container_record ={}
            container_record[Constants.RAKE_ID] = data[i].rake_id
            container_record[Constants.TRACK_NUMBER] = data[i].track_number
            container_record[Constants.RAKE_NUMBER]  = data[i].rake_number
            container_record[Constants.TRAIN_NUMBER]  = data[i].train_number
            container_record[Constants.RAKE_TYPE] = data[i].rake_type
            container_record[Constants.WAGON_LIST] = []
            wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].wagon_sequence_number}}
            container_record[Constants.WAGON_LIST].append(wagon_record)
            container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i].container_number}
            container_record[Constants.COMMIDITY]= data[i].attribute_2
            container_record[Constants.LINER_SEAL] = {Constants.VALUE : data[i].attribute_3}
            container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i].seal_number}
            container_record[Constants.POD] = data[i].container_destination_station
            container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i].iso_code if data[i].iso_code else str(data[i].container_size)+str(data[i].container_type) if data[i].container_size and data[i].container_type else None}
            container_record[Constants.LDD_MT_FLAG] = {Constants.VALUE : data[i].ldd_mt_flg} 
            container_record[Constants.KEY_SLINE_CODE] =  {Constants.VALUE : data[i].sline_code}
            container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:data[i].wagon_sequence_number}
            container_record[Constants.CONTAINER_STAT] = "E"
            container_record[Constants.CATEGORY] = "Import"

            response.append(container_record)
        return json.dumps(response)

    # @query_debugger()
    # def get_ctms_details(start_date,end_date):
    #     rake_query = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)>=start_date, cast(CCLSRake.trans_date, DATE)<=end_date).all()
    #     if rake_query:
    #         return RakeInwardReadService.format_cmts_data(rake_query)
    #     return rake_query
    

    @query_debugger()
    def get_ctms_train_no_details(train_no):
        rake_query = CCLSRake.query.filter_by(train_number=train_no).all()
        if rake_query:
            return RakeInwardReadService.format_cmts_data(rake_query)
        return rake_query
    
    @query_debugger()
    def ctms_details(start_date,end_date,train_no=None):
        if train_no:
            rake = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)>=start_date, cast(CCLSRake.trans_date, DATE)<=end_date)
            rake_query = rake.filter_by(train_number=train_no).all()
        else:
            rake_query = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)>=start_date, cast(CCLSRake.trans_date, DATE)<=end_date).all()
        if rake_query:
            return RakeInwardReadService.format_cmts_data(rake_query)
        return rake_query