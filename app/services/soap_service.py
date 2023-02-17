
import zeep
import config
from datetime import datetime
from app.models import CCLSRake
from app import postgres_db as db
from app.services.gt_upload_service import commit
import json


def get_permit_details(permit_number):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/EmpltyTrailer/emptytrailerbpel_client_ep?WSDL"
    
    try:
        # soap = zeep.Client(wsdl=wsdl_url, 
        #                 service_name="emptytrailerbpel_client_ep",
        #                 port_name="EmptyTrailerBPEL_pt")
        soap = zeep.Client(config.WSDL_FILE)
        result = soap.service.process(permit_number)
        print(result)
    except Exception as e:
        print(e)
        result = {}
    return result

def update_container_details(data):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/GateWriteOperation/gatewriteoperation_client_ep?WSDL"
    try:
        post_data = {}
        if "vehicle_no" in data:
            post_data['VEH_NO'] = data["vehicle_no"]
        if "user_id" in data:
            post_data["USER_ID"] = data["user_id"]  
        if "gate_no" in data:
            post_data["GATE_NO"] = data["gate_no"]      #max 3 digits
        if "stk_loc" in data:
            post_data["STK_LOC"] = data["stk_loc"]  
        if "container_no" in data:
           post_data["CTR_NO"] = data["container_no"]
        if "seal_no" in data:
           post_data["SEAL_NO"] = data["seal_no"] 
        if "dmg_code" in data:
            post_data["DMG_CODE"] = data["dmg_code"] 
        if "dt_seal" in data:    
            post_data["DT_SEAL"] = datetime.strptime(data["dt_seal"], '%Y-%m-%d %H:%M:%S')
        if "is_empty_or_laden" in data:
            post_data["CTR_STAT"] = "L" if data["is_empty_or_laden"]=="Laden" else "E" 
        if "gate_in_time" in data:
            post_data["DT_VEH_ARR"] = datetime.strptime(data["gate_in_time"], '%Y-%m-%d %H:%M:%S')
            post_data["ARR_PMT_NO"] = data["permit_no"] if "permit_no" in data else "TEST"
        if "gate_out_time" in data:
            post_data["DT_VEH_DEP"] = datetime.strptime(data["gate_out_time"], '%Y-%m-%d %H:%M:%S')
            post_data["DEP_PMT_NO"] = data["permit_no"] if "permit_no" in data else "TEST"
        
        post_data["SEAL_STAT"] = "Y" if ("seal_no" in data) and data["seal_no"] else "N"
        post_data["DMG_FLG"] =  "Y" if "damage_status" in data  and data["damage_status"] else "N"
        post_data["HAZ_FLG"] =  "Y" if "hazard_status" in data and data["hazard_status"] else "N" 

        print(post_data)
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="gatewriteoperation_client_ep",
                        port_name="GateWriteOperation_pt")
        
        
        result = soap.service.process(**post_data)
        print(result)
        
    except Exception as e:
        print(e)
        result = {}
    return result

def get_train_data(train_number='',from_date='', to_date = ''):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeReadOperation/rakereadproocess_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakereadproocess_client_ep",
                        port_name="RakeReadProocess_pt")
        rake_data = {'TrainNumber': train_number, 'From': from_date,'To':to_date }
        result = soap.service.process(**rake_data)
        # print(result)
        return result
    except Exception as e:
        print(e)
        result = {}
        return result