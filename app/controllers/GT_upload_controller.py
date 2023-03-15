from app.controllers.gate_controller import Model
from app.services.decorator_service import custom_exceptions, jwt_auth_required
from app.services.gt_upload_service import upload_ccls_rake_date, upload_pendancy_data

import xmltodict
import json
from flask import request,Response
from datetime import datetime

 
def get_xml_file_data_to_dict():
    input_file = request.files['file']
    xml_data = input_file.read()
    return xmltodict.parse(xml_data)
        

class TrainSummary(Model):
    @custom_exceptions
    def post(self):
        summary = get_xml_file_data_to_dict()
        if "RR_CTR_NOT_ARR" in summary:
            wagon_list = self.process_RR_summary(summary)
        elif "INWARD_TRAIN" in summary:
            wagon_list = self.process_inward_train_summary(summary)
        else:
            return Response(json.dumps({"message":"unknown file format"}),status=400,mimetype='application/json')
        if upload_ccls_rake_date(wagon_list):
            return Response(json.dumps({"message":"success"}),status=201,mimetype='application/json')
    
    def process_RR_summary(self,data):
        wagons_list = []
        train_details = data["RR_CTR_NOT_ARR"]["LIST_G_TRN_NO"]
        for each in train_details["G_TRN_NO"]:
            final_data = {}
            final_data["train_number"] = each["TRN_NO"]
            final_data["date_actual_departure"] = each["DT_ACT_DEP"]
            final_data["wagon_number"] = each["WGN_NO"]
            final_data["container_number"] = each["CTR_NO"]
            final_data["container_life_number"] = each["CTR_LIFE_NO"]
            final_data["container_size"] = each["CTR_SIZE"]
            final_data["sline_code"] = each["SLINE_CD"]
            final_data["wagon_sequence_number"] = each["CS_S_NO"]
            wagons_list.append(final_data)
        return wagons_list
            
    def process_inward_train_summary(self,data):
        wagons_list = []
        train_details =data["INWARD_TRAIN"]["LIST_G_TRN_NO"]["G_TRN_NO"]
        for wagon in train_details["LIST_G_WGN_NO"]["G_WGN_NO"]:
            final_data = {}
            final_data["train_number"] = train_details["TRN_NO"]
            final_data["train_origin_station"] = train_details["FRM_LOC"]
            final_data["date_actual_departure"] = train_details["DT_ACT_DEP"]
            final_data["wagon_number"] =  wagon["WGN_NO"]
            final_data["container_number"] = wagon["CTR_NO"]
            final_data["container_size"] = wagon["CTR_SIZE"]
            final_data["sline_code"] = wagon["SLINE_CD"]
            final_data["container_type"] = wagon["CTR_TYPE"]
            final_data["wagon_sequence_number"] = wagon["CS_COUNT"]
            final_data["ldd_mt_flg"] = wagon["LDD_MT_FLG"]
            final_data["adv_boe_flg"] = wagon["ADV_BOE_FLG"]
            wagons_list.append(final_data)
        return wagons_list
    
    
class PendancySummary(Model):
    @custom_exceptions
    def post(self):
        data = get_xml_file_data_to_dict()
        if "RR_EXP_LDD_LST" in data:
            container_list = self.process_pendancy_summary(data['RR_EXP_LDD_LST'])
        else:
            return Response(json.dumps({"message":"unknown file format"}),status=400,mimetype='application/json')
        if upload_pendancy_data(container_list):
            return Response(json.dumps({"message":"success"}),status=201,mimetype='application/json')
        
    def process_pendancy_summary(self,data):
        final_container_list = []
        gateway_port_list = data['LIST_G_GW_PORT_CD']['G_GW_PORT_CD']
        if isinstance(gateway_port_list,dict):
            gateway_port_list = [gateway_port_list]
        for port in gateway_port_list:
            gateway_port_code =  port["GW_PORT_CD"]
            data = self.process_each_gateway_port(port["LIST_G_CTR_NO"]["G_CTR_NO"],gateway_port_code)
            final_container_list+=data
        return final_container_list
    
    
    def process_each_gateway_port(self,data,port_code):
        container_list = []
        gateway_port_code =  port_code
        if isinstance(data,dict):
            data = [data]
        for pendancy_container in data:
            container = {}
            container["container_number"] = pendancy_container["CTR_NO"]
            if pendancy_container["CTR_LIFE_NO"]:
                container["container_life_number"] = datetime.strptime(pendancy_container["CTR_LIFE_NO"], '%d-%m-%Y %H:%M:%S') 
            container["container_stat"] = pendancy_container["CTR_STAT"]
            container["container_size"] = int(pendancy_container["CTR_SIZE"])
            container["container_type"] = pendancy_container["CTR_TYPE"]
            container["container_weight"] = float(pendancy_container["WT"])
            container["container_acty_code"] = pendancy_container["CTR_ACTY_CD"]
            container["icd_loc_code"] = pendancy_container["LOC_CD"]
            container["stuffed_at"] = pendancy_container["STF_AT"]
            container["stack_loc"] = pendancy_container["STK_LOC"]
            container["sline_code"] = pendancy_container["SLINE_CD"]
            container["gateway_port_code"] = gateway_port_code
            if pendancy_container["ARR_DATE"]:
                container["arrival_date"] =  datetime.strptime(pendancy_container["ARR_DATE"], '%d-%m-%Y %H:%M:%S')
            if pendancy_container["SEAL_DATE"]:
                container["seal_date"] =  datetime.strptime(pendancy_container["SEAL_DATE"], '%d-%m-%Y %H:%M:%S')
            container["odc_flag"] = pendancy_container["ODC_FLG"]
            container["hold_rels_flg"] = pendancy_container["HOLD_RELS_FLG"]
            container_list.append(container)
        return container_list