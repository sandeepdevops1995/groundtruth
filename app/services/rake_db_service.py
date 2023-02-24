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
            
        except:
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
            print(e)
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
            print(e)
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.post_track_details(data,count,isRetry)
    
    @query_debugger()
    def get_train_details(query_values,track_number=None,from_date=None,to_date=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
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
                data = CCLSRake.query.filter(cast(CCLSRake.trans_date, DATE)==query_values["trans_date"])
                query_values.pop('trans_date')
                data = data.filter_by(**query_values).order_by('trans_date').all()
            else:
                data = CCLSRake.query.filter_by(**query_values).order_by('trans_date').all()
            if data and track_number:
                from app.models import Track
                track_details = Track.query.filter(Track.track_no == track_number).first()
                if (track_details.trans_date == None ) or (track_details.trans_date <= data[0].trans_date) : 
                    track_details.train_no = data[0].train_number
                    track_details.trans_date = data[0].trans_date
                    commit()
                    logger.info("updated track details")
            return RakeDbService.format_rake_data(data)
            
        except Exception as e:
            print(e)
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
            "container_life_number" : wagon["container_life_number"],
            "trans_date" : wagon["trans_date"],
            "train_number" : wagon["train_number"]}
            wagon_model = CCLSRake(**wagon)
            final_data.append(wagon_model)
            try:
                result = CCLSRake.query.filter_by(**query_fields).all()
                if not result:
                    db.session.add(wagon_model)
                else:
                    print("wagon already exists in db")
            except Exception as e:
                print(e)
        try:
            commit()
        except Exception as e:
            print(e)
        
        return final_data

    def format_rake_data(data):
        response = {}
        if len(data)>0:
            response[Constants.TRACK_NUMBER] = data[0].attribute_1
            response[Constants.RAKE_NUMBER]  = data[0].rake_number
            response[Constants.TRAIN_NUMBER]  = data[0].train_number
            response[Constants.RAKE_TYPE] = data[0].rake_type
            response[Constants.WAGON_LIST] = []
            response[Constants.CONTAINER_LIST] = []
            for i in range(len(data)):
                wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : data[i].wagon_number,Constants.KEY_ID:data[i].wagon_sequence_number}}
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
                container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : data[i].wagon_number,Constants.KEY_ID:data[i].wagon_sequence_number}
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
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                RakeDbService.get_rake_details_by_track_number(track_number,rake_type,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE)


    def get_container_data(container_number):
        if config.GROUND_TRUTH == GroundTruthType.SOAP.value:
            pass
        data = CCLSRake.query.filter_by(container_number=container_number).all()
        if data:
            return RakeDbService.format_rake_data(data)
        else:
            return {}

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
        except SQLAlchemyError as exe:
                print(exe)
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
        except:
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
        except:
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
            print(e)
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
        except:
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
        except:
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
        except:
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
        except:
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
        except:
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
            
            
        except:
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
        except:
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
            
        except:
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
            
        except:
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
            
        except:
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
        except:
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
            
        except:
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
