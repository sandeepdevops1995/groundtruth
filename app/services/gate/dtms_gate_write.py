from app.services.decorator_service import query_debugger
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


class DTMSGateWriteService:

    def format_data_to_ccls_format(data,soap_data={}):
        if "factory_in_time" in data:
            soap_data[Constants.KEY_SOAP_G_DTMS_FACTORY_IN_TIME] = datetime.strptime(data["factory_in_time"], '%Y-%m-%d %H:%M:%S').isoformat() if data["factory_in_time"] else None
        if "factory_out_time" in data:
            soap_data[Constants.KEY_SOAP_G_DTMS_FACTORY_OUT_TIME] = datetime.strptime(data["factory_out_time"], '%Y-%m-%d %H:%M:%S').isoformat() if data["factory_out_time"] else None
        if "factory_reach_time" in data:
            soap_data[Constants.KEY_SOAP_G_DTMS_FACTORY_REACH_TIME] = datetime.strptime(data["factory_reach_time"], '%Y-%m-%d %H:%M:%S').isoformat() if data["factory_reach_time"] else None
        if "user_id" in data:
            soap_data[Constants.KEY_SOAP_G_DTMS_USER_ID] = data['user_id']
        if 'reason_code' in data:
            soap_data[Constants.KEY_SOAP_G_DTMS_REASON_CODE] = data['reason_code']
        if Constants.KEY_ATTRIBUTE1 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE1] = data['seal_no']
        if Constants.KEY_ATTRIBUTE2 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE2] = data[Constants.KEY_ATTRIBUTE2]
        if Constants.KEY_ATTRIBUTE3 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE3] = data[Constants.KEY_ATTRIBUTE3]
        if Constants.KEY_ATTRIBUTE4 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE4] = data[Constants.KEY_ATTRIBUTE4]
        if Constants.KEY_ATTRIBUTE5 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE5] = data[Constants.KEY_ATTRIBUTE5]
        if Constants.KEY_ATTRIBUTE6 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE6] = datetime.strptime(data[Constants.KEY_ATTRIBUTE6], '%Y-%m-%d %H:%M:%S').isoformat() if data[Constants.KEY_ATTRIBUTE6] else None
        if Constants.KEY_ATTRIBUTE7 in data:
            soap_data[Constants.KEY_SOAP_ATTRIBUTE7] = datetime.strptime(data[Constants.KEY_ATTRIBUTE7], '%Y-%m-%d %H:%M:%S').isoformat() if data[Constants.KEY_ATTRIBUTE7] else None
        if Constants.KEY_CREATED_AT in data:
            soap_data[Constants.KEY_SOAP_CREATED_AT] = datetime.strptime(data[Constants.KEY_CREATED_AT], '%Y-%m-%d %H:%M:%S').isoformat() if data[Constants.KEY_CREATED_AT] else None
        if Constants.KEY_CREATED_BY in data:
            soap_data[Constants.KEY_SOAP_CREATED_BY] = data[Constants.KEY_CREATED_BY]
        if Constants.KEY_UPDATED_AT in data:
            soap_data[Constants.KEY_SOAP_UPDATED_AT] = datetime.strptime(data[Constants.KEY_UPDATED_AT], '%Y-%m-%d %H:%M:%S').isoformat() if data[Constants.KEY_UPDATED_AT] else None
        if Constants.KEY_UPDATED_BY in data:
            soap_data[Constants.KEY_SOAP_UPDATED_BY] = data[Constants.KEY_UPDATED_BY]
        if Constants.KEY_ERROR_MSG in data:
            soap_data[Constants.KEY_SOAP_ERROR_MSG] = data[Constants.KEY_ERROR_MSG]
        if Constants.KEY_STATUS_FLG in data:
            soap_data[Constants.KEY_SOAP_STATUS_FLG] = data[Constants.KEY_STATUS_FLG]
        if Constants.KEY_READ_FLG in data:
            soap_data[Constants.KEY_SOAP_READ_FLG] = data[Constants.KEY_READ_FLG]


    def get_dtms_soap_format_for_truck(data):
        try:
            soap_data = {}
            soap_data[Constants.KEY_SOAP_G_DTMS_GATEPASS_NUMER] = data['permit_no']
            soap_data[Constants.KEY_SOAP_G_DTMS_VEH_NUMBER] = data['vehicle_no']
            if "gate_out_time" in data:
                soap_data[Constants.KEY_SOAP_G_DTMS_IN_OUT_TIMEOUT] = datetime.strptime(data['gate_out_time'], '%Y-%m-%d %H:%M:%S').isoformat() if data['gate_out_time'] else None
                soap_data[Constants.KEY_SOAP_G_DTMS_CTR_IN_OUT_FLAG] = 'O'
            elif "gate_in_time" in data:
                soap_data[Constants.KEY_SOAP_G_DTMS_IN_OUT_TIMEIN] = datetime.strptime(data['gate_in_time'], '%Y-%m-%d %H:%M:%S').isoformat() if data['gate_in_time'] else None
                soap_data[Constants.KEY_SOAP_G_DTMS_CTR_IN_OUT_FLAG] = 'I'
            soap_data[Constants.KEY_SOAP_G_DTMS_CARGO_CONTAINER_FLAG] = 'T'
            # soap_data[Constants.KEY_SOAP_G_DTMS_CARGO_LDD_EMPTY_FLAG_VEH] = "L" if data["is_empty_or_laden"]=="Laden" else "E"
            DTMSGateWriteService.format_data_to_ccls_format(data,soap_data)
            return soap_data
        except Exception as e:
            logger.exception(str(e))
        
        

    def get_dtms_soap_format_for_container(data):
        try:
            soap_data = {}
            soap_data[Constants.KEY_SOAP_G_DTMS_GATEPASS_NUMER] = data['permit_no']
            soap_data[Constants.KEY_SOAP_G_DTMS_VEH_NUMBER] = data['vehicle_no']
            soap_data[Constants.KEY_SOAP_G_DTMS_CTR_NUMBER] = data['container_no']
            soap_data[Constants.KEY_SOAP_G_DTMS_CTR_SIZE] = data['container_size']
            # soap_data[Constants.KEY_SOAP_G_DTMS_HAZARD_STATUS] = data['hazard_status']
            soap_data[Constants.KEY_SOAP_G_DTMS_HAZARD_STATUS] = "N"
            ctr_type = str(data['container_size']) + data['container_type']
            soap_data[Constants.KEY_SOAP_G_DTMS_CTR_TYPE] = ctr_type if len(ctr_type) <= 4 else data['container_type']
            soap_data[Constants.KEY_SOAP_G_DTMS_DAMAGE_STATUS] = "Y" if "damage_status" in data  and data["damage_status"] else "N"        
            if "gate_out_time" in data:
                soap_data[Constants.KEY_SOAP_G_DTMS_IN_OUT_TIMEOUT] = datetime.strptime(data['gate_out_time'], '%Y-%m-%d %H:%M:%S').isoformat() if data['gate_out_time'] else None
                soap_data[Constants.KEY_SOAP_G_DTMS_CTR_IN_OUT_FLAG] = 'O'
            elif "gate_in_time" in data:
                soap_data[Constants.KEY_SOAP_G_DTMS_IN_OUT_TIMEIN] = datetime.strptime(data['gate_in_time'], '%Y-%m-%d %H:%M:%S').isoformat() if data['gate_in_time'] else None
                soap_data[Constants.KEY_SOAP_G_DTMS_CTR_IN_OUT_FLAG] = 'I' 
            soap_data[Constants.KEY_SOAP_G_DTMS_CARGO_CONTAINER_FLAG] = 'C'
            soap_data[Constants.KEY_SOAP_G_DTMS_CTR_LDD_EMPTY_FLAG] = "L" if data["is_empty_or_laden"]=="Laden" else "E"
            DTMSGateWriteService.format_data_to_ccls_format(data,soap_data)
            return soap_data
        except Exception as e:
            logger.exception(str(e))
