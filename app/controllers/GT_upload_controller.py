from app.controllers.gate_controller import Model
from app.services.decorator_service import custom_exceptions, jwt_auth_required
from app.services.gt_upload_service import upload_ccls_rake_date

import xmltodict
import json
from flask import request,Response

 
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