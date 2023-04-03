import app.constants as Constants
import config
from datetime import datetime, date
import json
from datetime import datetime, timedelta
from sqlalchemy.sql import text
import os
from app import engine as e
from app.services.decorator_service import query_debugger
from app.services import soap_service
from app.constants import GroundTruthType
from app.models import Permit
from app.models.utils import db_format,db_functions
from app.logger import logger
from app import postgres_db
import random
import time

class GateDbService:
    def get_details_by_container_number(self,container_number):
        result = self.get_container_info(container_number)
        return result

    @query_debugger()
    def get_container_info(self,container_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"get_ctr_dtls.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,container_number=container_number)
            sqlFile.close()
            conn.close()
            data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            for ctr in data:
                if(ctr['permit_no'].startswith('PMA')):
                    if(ctr['date_arr'] is None):
                        return self.send_formated_date_ctr_info(ctr)        
                elif(ctr['permit_no'].startswith('PMD')):
                    if(ctr['date_dept'] is None):
                        return self.send_formated_date_ctr_info(ctr)
            for ctr in data:
                if(ctr['validity'] > datetime.now()):
                    return self.send_formated_date_ctr_info(ctr)       
            if (len(data)>1): 
                return self.send_formated_date_ctr_info(data[0])

            return json.dumps({})       
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.get_container_info(container_number,count,isRetry)

    def send_formated_date_ctr_info(self,data):
        data['validity'] = data['validity'].strftime('%d-%m-%Y %H:%M:%S')
        data['bill_info'] = self.get_bill_info(data['ctr_no'])
        return json.dumps([data])

    def get_bill_info(self,container_number):
        conn = e.connect()
        billFile = open(os.path.join(config.SQL_DIR,"get_pmt_bill_details.sql"))
        bill_cmd = text(billFile.read())
        bill_query = conn.execute(bill_cmd,container_number=container_number)
        billFile.close()
        bill_data = [dict(zip(tuple (bill_query.keys()) ,i)) for i in bill_query.cursor]
        return bill_data


    def get_details_by_crn_number(self,crn_number):
        result = self.get_crn_info(crn_number)
        return result                                                                                                       
    
    @query_debugger()
    def get_crn_info(self,crn_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"get_crn_dtls.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,crn_number=crn_number)
            sqlFile.close()
            conn.close()
            data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            for ctr in data:
                conn = e.connect()
                billFile = open(os.path.join(config.SQL_DIR,"get_pmt_bill_details.sql"))
                bill_cmd = text(billFile.read())
                bill_query = conn.execute(bill_cmd,container_number=ctr['ctr_no'])
                billFile.close()
                bill_data = [dict(zip(tuple (bill_query.keys()) ,i)) for i in bill_query.cursor]
                ctr['bill_info'] = bill_data 
            return json.dumps(data)     
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.get_crn_info(crn_number,count,isRetry)
    
    @query_debugger()                  
    def get_details_permit_number(self,permit_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"get_ctr_info_frm_pmt.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,permit_number=permit_number) 
            
            sqlFile.close()
            conn.close()
            data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            if data:
                info=data[0]
                conn = e.connect()
                billFile = open(os.path.join(config.SQL_DIR,"get_pmt_bill_details.sql"))
                bill_cmd = text(billFile.read())
                bill_query = conn.execute(bill_cmd,container_number=info['container_no']) 
                billFile.close()
                info['POD'] = info['pod']
                truckFile = open(os.path.join(config.SQL_DIR,"get_truck_dtls.sql"))
                truck_cmd = text(truckFile.read())
                truck_query = conn.execute(truck_cmd)
                truckFile.close()
                conn.close()
                bill_data = [dict(zip(tuple (bill_query.keys()) ,i)) for i in bill_query.cursor]
                info['bill_info'] = bill_data
                truck_data = [dict(zip(tuple (truck_query.keys()) ,i)) for i in truck_query.cursor]
                info['truck'] = truck_data[0]
                info.pop('gt_truck_no')
                info['hazard'] = ['Class_8']
                info['un_number'] = ['2928']
                return json.dumps(info)
            return json.dumps({})
        elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
            result = soap_service.get_permit_details(permit_number)
            if result:
                if result['PermitDateTime'] and isinstance(result['PermitDateTime'], datetime):
                    result['PermitDateTime']=result['PermitDateTime'].strftime("%Y-%m-%d %H:%M:%S")
                if result['CtrLifeNumber'] and isinstance(result['CtrLifeNumber'], date):
                    result['CtrLifeNumber']=result['CtrLifeNumber'].strftime("%Y-%m-%d")
                if result['ContainerSize'] and  result['ContainerType']:
                    iso_code = str(result['ContainerSize'])+str(result['ContainerType'])
                else:
                    iso_code = None
                final_data = {
                                "permit_no":result['PermitNumber'],
                                "permit_date":result['PermitDateTime'],
                                "permit_expiry_date":result['IsPermitValid'],
                                "container_no":result['ContainerNumber'],
                                "vehicle_no" : result['VechileNumber'],
                                "sline_code" : result['SlineCode'],
                                "container_status" : result['ContainerStatus'],
                                "container_type" : result['ContainerType'],
                                "container_size" : result['ContainerSize'],
                                "container_life_no" : result['CtrLifeNumber'],
                                "health" : result['DamageStatus'],
                                "gate_in_time" : result['VehicleGateInDateTime'],
                                "iso_code": iso_code,
                                "is_empty_or_laden": "Empty" if "E" in result['ContainerStatus'] else "Laden",
                                "pod":None,
                                "cargo_type":None,
                                "liner_seal":None,
                                "custom_seal":None,
                                "reefer":None,
                                "permit_type":None,
                                "permit_details":{"container_life_no" : result['CtrLifeNumber'],
                                                  "container_status" : result['ContainerStatus'],
                                                  "sline_code" : result['SlineCode']
                                                  },
                                "POD":None,
                                "bill_info":[ {
                                        "bill_no":None,
                                        "bill_type":None,
                                        "bill_details":None,
                                        "ctr_no":result['ContainerNumber']
                                    },],
                                "truck":{
                                    "gt_truck_no":result['VechileNumber'],
                                    "driver_name":None,
                                    "driver_number":None,
                                    "driver_license":None
                                },
                                "hazard":[],
                                "un_number":[]
                            }
                if result['ContainerStatus']:
                    final_data['is_empty_or_laden']= "Empty" if "E" in result['ContainerStatus'] else "Laden"
                if final_data:
                    return json.dumps(final_data)
          
        pmt_details = Permit.query.filter_by(permit_no=permit_number).first()
        if pmt_details:
            logger.info('GT,Fetched from Postgres DB - permit number: {}'.format(permit_number))
            return db_functions(pmt_details).as_json()
        return None


    def add_container(containers_list):
        pass

    def save_containers_data(container_data):
        if container_data:
            data = GateDbService.AutoFill()
            if Constants.PERMIT_NUMBER in container_data:
                data[Constants.PERMIT_NUMBER] = container_data[Constants.PERMIT_NUMBER]
            if Constants.CONTAINER_NUMBER  in container_data:
                data[Constants.CONTAINER_NUMBER] = container_data[Constants.CONTAINER_NUMBER]
            if Constants.TRUCK_NUMBER  in container_data:
                data[ Constants.TRUCK][Constants.TRUCK_NUMBER] = container_data[Constants.TRUCK_NUMBER]
                data[Constants.VEHICLE_NUMBER] = container_data[Constants.TRUCK_NUMBER]
            if Constants.ISO_CODE  in container_data:
                data[Constants.ISO_CODE] = container_data[Constants.ISO_CODE]
            if Constants.PERMIT_EXPIRY_DATE in container_data:
                data[Constants.PERMIT_EXPIRY_DATE] = datetime.strptime(container_data[Constants.PERMIT_EXPIRY_DATE], '%Y-%m-%d %H:%M:%S')
            permit_data = Permit(**db_format(data))
            postgres_db.session.add(permit_data)
            postgres_db.session.commit()
            return data
        return False
    
        
    def save_ctr_permit_records(records_count):
        if records_count:
            for i in range(int(records_count)):
                data = GateDbService.AutoFill()
                try:
                    permit_data = Permit(**db_format(data))
                    postgres_db.session.add(permit_data)
                    
                except Exception as e:
                    print("Exception",e)
                    i = i+1
                    continue

            postgres_db.session.commit()
            return True
        return False

           
    def AutoFill():
        number1 = random.randint(10,99)
        number2 = random.choice(['FN',"TY","ER","TZ","FK","QZ","NL","CV"])
        number3 = random.randint(1000,9999)
        lpn_number = "TS" + str(number1) + str(number2) + str(number3)
        ctr_number = random.choice(["NOSU2315713","INBU3483107","UGMU8524827","IEAU2532562","UXXU4303169","GATU0435213","UXXU2237387","BLJU2963369","MOLU2437931","NOSU2209795","UXXU2222746","NOSU2348492","TTNU2686813","YMLU2756984","APLS2969522","CRXU1315968","NOSU2465837","CRXU2282489","UGMU8769368","CAXU2094770","APLS294676","APLS292792","MAEU6751114","MAEU6347231","UACU4884735","LMCU1102790","PONU7446330","NYKU5408041","PONU7419289","NOSU4374593","CPSU4738530","TRLU5267390","TEXU2819286","TEXU3533379","MLCU2261835","TEXU2318469","NSAU2043292","TEXU3819296","CRXU9158778","MAEU7653642","TGHU2139116","MSCU2339670","ZCSU8155312","TRLU5240104","KKTU7159698","KKTU7226245","TRLU5227669","TRLU5232351","TRLU5235176","TRLU5209161","GATU8302942","TTNU9599330","TRLU5217892","ICSU6924160","PONU7152422","MLCU4858007","POCU1057830","PONU7108137","INKU2654091","PONU7396497","TOLU3903429","PCIU3569665","GATU0206393","TRLU5192182","TTNU2100141","OCLU1190547","CAXU6016250","NYKU2368407","TGHU2308920","KLTU1156822","TRLU5207636"])
        container_size = random.choice(['20','40'])
        container_type = "GL"
        container_status = random.choice(["IL","E"])
        sline_code  = random.choice(["PALI","TCMP","BEN","TSSL","NOV","ECT","WMS","ASL","SML","TIGR","USS","ASW","SRS","IGM"])
        permit_date = datetime.now()
        permit_expiry_date = permit_date + timedelta(days = 730)
        # Permit Number Generation
        number = random.randint(111111,999999)
        permit = random.choice(['PMA','PMD'])
        
        data = {
            Constants.PERMIT_NUMBER:permit+str(number),
            Constants.PERMIT_DATE: permit_date,
            Constants.PERMIT_EXPIRY_DATE: permit_expiry_date,
            Constants.CONTAINER_NUMBER: ctr_number,
            Constants.CONTAINER_SIZE : container_size,
            Constants.CONTAINER_TYPE : container_type,
            Constants.CONTAINER_STATUS : container_status,
            Constants.HAZARD_STATUS : False,
            Constants.DAMAGE_STATUS : False,
            Constants.KEY_SLINE_CODE : sline_code,
            Constants.GATE_IN_TIME: None,
            Constants.ISO_CODE: None,
            Constants.PERMIT_TYPE:None,
            Constants.LINER_SEAL:None,
            Constants.CUSTOM_SEAL:None,
            Constants.REFEER_TEMPERATURE:None,
            Constants.CARGO_TYPE:None,
            Constants.POD:None,
            Constants.IS_EMPTY_OR_LADEN: "Empty" if "E" in container_status else "Laden",
            Constants.VEHICLE_NUMBER : lpn_number,
            Constants.PERMIT_DETAILS : {},

            # Constants.PERMIT_DETAILS : {Constants.CONTAINER_LIFE_NO : None,
            #                             Constants.CONTAINER_STATUS : container_status,
            #                             Constants.KEY_SLINE_CODE : sline_code},
            Constants.BILL_INFO : { Constants.BILL_NUMBER:None,
                                    Constants.BILL_TYPE:None,
                                    Constants.BILL_DETAILS : None,
                                    Constants.CTR_NO : ctr_number },
            Constants.TRUCK : {Constants.GT_TRUCK_NUMBER: lpn_number,
                               Constants.DRIVER_NAME : None,
                               Constants.DRIVER_NUMBER : None,
                               Constants.DRIVER_LICENSE : None,},
            Constants.HAZARD : [],
            Constants.UN_NUMBER : [],
        }
        return data

    @query_debugger()
    def update_gateIn_info(self,container_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"update_gatein_dtls.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,container_number=container_number)
            sqlFile.close()
            conn.close()
            return query.keys()     
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.update_gateIn_info(container_number,count,isRetry)

    @query_debugger()
    def update_gateOut_info(self,container_number,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"update_gateout_dtls.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,container_number=container_number)
            sqlFile.close()
            conn.close()
            return query.keys()     
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.update_gateOut_info(container_number,count,isRetry)

    @query_debugger()
    def update_container_info(self,data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                conn = e.connect()
                if data['seal_no'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_seal_no.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],seal_no=data['seal_no'])
                    sqlFile.close()
                if data['sline_code'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_sline_code.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],sline_code=data['sline_code'])
                    sqlFile.close()
                if data['iso_code'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_iso_code.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],iso_code=data['iso_code'])
                    sqlFile.close()
                if data['dmg_code'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_dmg_code.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],dmg_code=data['dmg_code'])
                    sqlFile.close()
                if data['dmg_flg'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_dmg_flg.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],dmg_flg=data['dmg_flg'])
                    sqlFile.close()
                if data['ctr_type'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_ctr_type.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],ctr_type=data['ctr_type'])
                    sqlFile.close()
                if data['ctr_size'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_ctr_size.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],ctr_size=data['ctr_size'])
                    sqlFile.close()
                if data['ctr_ht'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_ctr_ht.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],ctr_ht=data['ctr_ht'])
                    sqlFile.close()
                if data['empty_laden'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_empty_laden.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],empty_laden=data['empty_laden'])
                    sqlFile.close()
                if data['icd_loc'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_icd_loc.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],icd_loc=data['icd_loc'])
                    sqlFile.close()
                if data['stk_loc'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_stk_loc.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],stk_loc=data['stk_loc'])
                    sqlFile.close()
                if data['import_export'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_import_export.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],import_export=data['import_export'])
                    sqlFile.close()
                if data['user_id'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_user_id.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],user_id=data['user_id'])
                    sqlFile.close()
                if data['seal_stat'] !="" :
                    sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_seal_stat.sql"))
                    command = text(sqlFile.read())
                    query = conn.execute(command,container_number=data['container_number'],seal_stat=data['seal_stat'])
                    sqlFile.close()
                conn.close()
                return query.keys()     
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                if data["is_container_trailer"]:
                    update_data = GateDbService.get_soap_format_for_container(data)
                else:
                    update_data = GateDbService.get_soap_format_for_truck(data)
                if update_data:
                    result= soap_service.update_container_details(update_data)
                else:
                    logger.info('GT, please check whether required keys available or not')
                if result:
                    logger.info('GT, Updated in soap service')
                    return True
            permit = Permit.query.filter_by(permit_no=data["permit_no"]).update(data)
            postgres_db.session.commit()
            if permit:
                return True
            else:
                return False
            
        except Exception as e:
            print(e)
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.update_container_info(data,count,isRetry)
    
    def get_soap_format_for_truck(data):
        post_data = {}
        try:
            post_data[Constants.KEY_SOAP_G_VEH_NO] = data["vehicle_no"]
            post_data[Constants.KEY_SOAP_G_GT_DOC_NO] = data["permit_no"]
            post_data[Constants.KEY_SOAP_G_DT_GT_DOC] = datetime.strptime(data["permit_date"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_DT_GT_DOC_VLD] =  datetime.strptime(data["permit_expiry_date"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_USER_ID] = data["user_id"]
            post_data[Constants.KEY_SOAP_G_SLINE_CD] = data["sline_code"]
            post_data[Constants.KEY_SOAP_G_XPMT_NO] = data["permit_no"]
            post_data[Constants.KEY_SOAP_G_DT_XPMT_NO] = data["permit_no"]
            post_data[Constants.KEY_SOAP_G_GATE_NO] = data["gate_no"] 
            post_data[Constants.KEY_SOAP_G_STK_LOC] = data["stk_loc"] 
            if "gate_in_time" in data:
                post_data[Constants.KEY_SOAP_G_DT_VEH_ARR] = datetime.strptime(data["gate_in_time"], '%Y-%m-%d %H:%M:%S')
                post_data[Constants.KEY_SOAP_G_DT_ARR] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
            if "gate_out_time" in data:
                post_data[Constants.KEY_SOAP_G_DT_VEH_DEP] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
                post_data[Constants.KEY_SOAP_G_DT_DEP] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
            return post_data
        except Exception as e:
            logger.exception(str(e))


    def get_soap_format_for_container(data):
        post_data = {}
        try:
            post_data[Constants.KEY_SOAP_G_VEH_NO] = data["vehicle_no"]
            post_data[Constants.KEY_SOAP_G_GT_DOC_NO] =  data["permit_no"]
            post_data[Constants.KEY_SOAP_G_DT_GT_DOC] =  datetime.strptime(data["permit_date"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_DT_GT_DOC_VLD] = datetime.strptime(data["permit_expiry_date"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_SEAL_STAT] = "Y" if ("seal_no" in data) and data["seal_no"] else "N"
            post_data[Constants.KEY_SOAP_G_SEAL_NO] = data["seal_no"] 
            post_data[Constants.KEY_SOAP_G_DMG_FLG] = "Y" if "damage_status" in data  and data["damage_status"] else "N"
            post_data[Constants.KEY_SOAP_G_DMG_CODE] = data["damage_code"]
            post_data[Constants.KEY_SOAP_G_CTR_NO] = data["container_no"]
            post_data[Constants.KEY_SOAP_G_CTR_SIZE]= data["container_size"]
            post_data[Constants.KEY_SOAP_G_CTR_TYPE] = data["container_type"]
            post_data[Constants.KEY_SOAP_G_CTR_STAT] = "L" if data["is_empty_or_laden"]=="Laden" else "E" 
            post_data[Constants.KEY_SOAP_G_USER_ID] = data["user_id"]
            post_data[Constants.KEY_SOAP_G_SLINE_CD] = data["sline_code"]
            post_data[Constants.KEY_SOAP_G_GATE_NO] = data["gate_no"] 
            post_data[Constants.KEY_SOAP_G_CTR_LIFE_NO] = datetime.strptime(data["container_life_no"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_DT_SEAL] = datetime.strptime(data["dt_seal"], '%Y-%m-%d %H:%M:%S')
            post_data[Constants.KEY_SOAP_G_HAZ_FLG] = "Y" if "hazard_status" in data and data["hazard_status"] else "N" 
            post_data[Constants.KEY_SOAP_G_STK_LOC] = data["stk_loc"] 
            if "gate_in_time" in data:
                post_data[Constants.KEY_SOAP_G_DT_VEH_ARR] = datetime.strptime(data["gate_in_time"], '%Y-%m-%d %H:%M:%S')
                post_data[Constants.KEY_SOAP_G_ARR_PMT_NO] = data["permit_no"] if "permit_no" in data else "TEST"
                post_data[Constants.KEY_SOAP_G_DT_ARR] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
            if "gate_out_time" in data:
                post_data[Constants.KEY_SOAP_G_DT_VEH_DEP] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
                post_data[Constants.KEY_SOAP_G_DEP_PMT_NO] = data["permit_no"] if "permit_no" in data else "TEST"
                post_data[Constants.KEY_SOAP_G_DT_DEP] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
            return post_data
        except Exception as e:
            logger.exception(str(e))
        

    @query_debugger()
    def update_ctr_stack_info(self,data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            conn = e.connect()
            if data['stk_loc'] !="" :
                sqlFile = open(os.path.join(config.SQL_DIR,"update_ctr_stk_loc.sql"))
                command = text(sqlFile.read())
                query = conn.execute(command,container_number=data['container_number'],stk_loc=data['stk_loc'])
                sqlFile.close()
            conn.close()
            return query.keys()     
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.update_ctr_stack_info(data,count,isRetry)

def Key_Mapping(j_data):
    record ={}
    temp ={}
    temp2 ={}
    if(Constants.PERMIT_NUMBER in j_data.keys()):
        record[Constants.PERMIT_NUMBER] = j_data[config.PERMIT_NUMBER]
    else:
        record[Constants.PERMIT_NUMBER] = ""
    
    if(Constants.PERMIT_TYPE in j_data.keys()):
        record[Constants.PERMIT_TYPE] = j_data[config.PERMIT_TYPE]
    else:
        record[Constants.PERMIT_TYPE] = ""
    
    record[Constants.PERMIT_DETAILS] = {}
    if(Constants.CONTAINER_NUMBER in j_data.keys()):
        record[Constants.CONTAINER_NUMBER] = j_data[config.CONTAINER_NUMBER]
    else:
        record[Constants.CONTAINER_NUMBER] = ""
    
    if(Constants.GT_TRUCK_NUMBER in j_data.keys()):
        temp2[Constants.GT_TRUCK_NUMBER] = j_data[config.GT_TRUCK_NUMBER]
        temp2[Constants.DRIVER_NAME]  = j_data[config.DRIVER_NAME]
        temp2[Constants.DRIVER_NUMBER] = str(j_data[config.DRIVER_NUMBER])
        temp2[Constants.DRIVER_LICENSE] = j_data[config.DRIVER_LICENSE]
        record[Constants.TRUCK_DETAILS] = temp2
    else:
        record[Constants.GT_TRUCK_NUMBER] = ""
    
    if(Constants.ISO_CODE in j_data.keys()):
        record[Constants.ISO_CODE] = j_data[config.ISO_CODE]
    else:
        record[Constants.ISO_CODE] = ""
    
    if(Constants.LINER_SEAL in j_data.keys()):
        record[Constants.LINER_SEAL] = str(j_data[config.LINER_SEAL])
    else:
        record[Constants.LINER_SEAL] = ""
    
    if(Constants.CUSTOM_SEAL in j_data.keys()):
        record[Constants.CUSTOM_SEAL] = str(j_data[config.CUSTOM_SEAL])
    else:
        record[Constants.CUSTOM_SEAL] = ""

    if(Constants.REFEER_TEMPERATURE in j_data.keys()):
        record[Constants.REFEER_TEMPERATURE] = j_data[config.REFEER_TEMPERATURE]
    else:
        record[Constants.REFEER_TEMPERATURE] = ""
    
    if(config.IS_EMPTY in j_data.keys()):
        record[Constants.IS_EMPTY] = j_data[config.IS_EMPTY]
    else:
        record[Constants.IS_EMPTY] = ""
    if(Constants.CARGO_TYPE in j_data.keys()):
        record[Constants.CARGO_TYPE] = j_data[config.CARGO_TYPE]
    else:
        record[Constants.CARGO_TYPE] = ""
    
    if(Constants.POD in j_data.keys()):
        record[Constants.POD] = j_data[config.POD]
    else:
        record[Constants.POD] = ""
    
    if(Constants.BILL_NUMBER in j_data.keys()):
        temp[Constants.BILL_NUMBER] = j_data[config.BILL_NUMBER]
        temp[Constants.BILL_TYPE]   = j_data[config.BILL_TYPE]
        temp[Constants.BILL_DATE]   = (datetime.now()- timedelta(days=1)).strftime(Constants.TIME_FORMAT) 
        record[Constants.BILL_INFO] = temp
    else:
        record[Constants.BILL_INFO] = ""
    
    if(Constants.IS_ONE_DOOR_OPEN in j_data.keys()):
        record[Constants.IS_ONE_DOOR_OPEN]    = j_data[config.IS_ONE_DOOR_OPEN]
    else:
        record[Constants.IS_ONE_DOOR_OPEN]    = ""

    if(Constants.IS_RFID_SEAL in j_data.keys()):
        record[Constants.IS_RFID_SEAL] = j_data[config.IS_RFID_SEAL]
    else:
        record[Constants.IS_RFID_SEAL] = ""
  
    record[Constants.PERMIT_DATE]           = datetime.now().strftime(Constants.TIME_FORMAT)
    record[Constants.PERMIT_EXPIRY_DATE]    = (datetime.now()+ timedelta(days=1)).strftime(Constants.TIME_FORMAT)  
    return  record

class Iso6346CodeService:
    @query_debugger()
    def validate(self,iso_code,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            try:
                ctrType = Constants.ISO_CCLS_TYPE_MAPPING[iso_code[2:4]]
                ctrSize = Constants.ISO_CCLS_SIZE_MAPPING[iso_code[0]]
            except:
                message = "No mapping for this ISO code "+ iso_code +" in CCLS"
                return json.dumps({"message":message})
            conn = e.connect()
            sqlFile = open(os.path.join(config.SQL_DIR,"get_iso_code.sql"))
            command = text(sqlFile.read())
            query = conn.execute(command,ctr_type=ctrType,ctr_size=ctrSize)
            sqlFile.close()
            conn.close()
            data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            if len(data):
                data[0][Constants.CONTAINER_HEIGHT] = Constants.ISO_CCLS_HEIGHT_MAPPING[iso_code[1]]
                return json.dumps(data[0])
            message = "No mapping for this ISO code "+ iso_code +" in CCLS"
            return json.dumps({"message":message})
        except:
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                self.validate(iso_code,count,isRetry)

