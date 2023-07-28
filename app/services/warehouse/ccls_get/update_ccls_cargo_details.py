import time
from app.enums import JobOrderType, ContainerFlag
from datetime import datetime
from app.controllers.utils import convert_ccls_date_to_timestamp, datetime_handler
import app.services.warehouse.constants as constants
import json

class UpdateCargoDetails(object):

    def update_carting_details_schema_for_serializer(self,cargo_details):
        container_info, carting_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["crn_number","crn_date","carting_order_number","con_date","is_cargo_card_generated","cha_code","gw_port_code","party_code","reserve_flag","max_date_unloading","contractor_job_order_no","contractor_job_order_date","exporter_name"]])
        cargo_details['container_info'] = json.loads(json.dumps(cargo_details['Container_details'], default=datetime_handler))[0] if 'Container_details' in cargo_details and cargo_details['Container_details'] else container_info
        cargo_details['carting_details'] = carting_details
        return cargo_details
    
    def update_stuffing_details_schema_for_serializer(self,cargo_details):
        container_info, stuffing_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["container_number","stuffing_job_order","cargo_weight_in_crn","crn_number","gw_port_code"]])
        cargo_details['container_info'] = container_info
        cargo_details['stuffing_details'] = stuffing_details
        return cargo_details
    
    def update_destuffing_details_schema_for_serializer(self,cargo_details):
        container_info, destuffing_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["container_number","destuffing_job_order","destuffing_plan_date","hld_rls_flag"]])
        cargo_details['container_info'] = container_info
        cargo_details['destuffing_details'] = destuffing_details
        return cargo_details
    
    def update_delivery_details_schema_for_serializer(self,cargo_details):
        container_info, delivery_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["gpm_number","gpm_valid_date","gpm_created_date","gp_stat","cha_code"]])
        cargo_details['container_info'] = container_info
        cargo_details['delivery_details'] = delivery_details
        return cargo_details
    
    def update_params(self,cargo_details,job_type,container_flag):
        cargo_details['job_type'] = job_type
        cargo_details['fcl_or_lcl'] = container_flag

    def update_truck_details(self,cargo_details):
        if 'truck_details' in cargo_details:
            truck_details = cargo_details['truck_details']
            for i in range(0,len(truck_details)):
                if 'truck_arrival_date' not in truck_details[i]:
                    truck_details[i]['truck_arrival_date'] = int(time.time())*1000
                if truck_details[i]['truck_number'] is None:
                    del truck_details[i]

    def update_container(self,cargo_details):
        if 'container_life' not in cargo_details or cargo_details["container_life"] is None:
            cargo_details["container_life"]=int(time.time())*1000
        if cargo_details['container_life'] and isinstance(cargo_details['container_life'], datetime):
            cargo_details['container_life']=convert_ccls_date_to_timestamp(cargo_details['container_life'])
        if cargo_details['container_life'] and isinstance(cargo_details['container_life'], str):
            cargo_details['container_life']=int(float(cargo_details['container_life']))
        cargo_details['container_size'] = cargo_details['container_size'] if 'container_size' in cargo_details else None
        if cargo_details['container_size'] and isinstance(cargo_details['container_size'], str):
            cargo_details['container_size'] = int(float(cargo_details['container_size']))

    def update_each_bill(self,each_bill):
        if each_bill[constants.CCLS_COMMODITY_CODE] and isinstance(each_bill[constants.CCLS_COMMODITY_CODE], str):
            each_bill[constants.CCLS_COMMODITY_CODE] = int(each_bill[constants.CCLS_COMMODITY_CODE])
        if each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED] and isinstance(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED], str):
            each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED] = int(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED])
        if each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED] is None:
            each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED] = 0
        if each_bill['package_weight']:
            each_bill['package_weight'] = float(each_bill['package_weight'])
        else:
            each_bill['package_weight'] = 0

    def update_shipping_bill_details(self,cargo_details):
        cargo_details['shipping_bill_details_list'] = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cargo_details['shipping_bill_details_list'])]
        for each_bill in cargo_details['shipping_bill_details_list']:
            if each_bill[constants.CCLS_SHIPPING_BILL_DATE] and isinstance(each_bill[constants.CCLS_SHIPPING_BILL_DATE],datetime):
                each_bill[constants.CCLS_SHIPPING_BILL_DATE] = convert_ccls_date_to_timestamp(each_bill[constants.CCLS_SHIPPING_BILL_DATE])
            self.update_each_bill(each_bill)

    def update_bill_details(self,cargo_details,container_flag):
        cargo_details['bill_details_list'] = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cargo_details['bill_details_list'])]
        for each_bill in cargo_details['bill_details_list']:
            if 'bill_number' in each_bill:
                bill_number = each_bill.pop('bill_number')
                #if container_flag==ContainerFlag.FCL.value:
                each_bill['boe_number'] = bill_number
                #else:
                each_bill['bol_number'] = bill_number
            if constants.CCLS_BOL_DATE in each_bill:
                if each_bill[constants.CCLS_BOL_DATE] and isinstance(each_bill[constants.CCLS_BOL_DATE],datetime):
                    each_bill[constants.CCLS_BOL_DATE] = convert_ccls_date_to_timestamp(each_bill[constants.CCLS_BOL_DATE])
            if each_bill[constants.CCLS_BILL_DATE] and isinstance(each_bill[constants.CCLS_BILL_DATE],datetime):
                each_bill[constants.CCLS_BILL_DATE] = convert_ccls_date_to_timestamp(each_bill[constants.CCLS_BILL_DATE])
            if constants.CCLS_BOL_DATE not in each_bill:
                each_bill[constants.CCLS_BOL_DATE] = each_bill[constants.CCLS_BILL_DATE]
            self.update_each_bill(each_bill)

    def update_carting_details(self,cargo_details,job_type,crn_number):
        if cargo_details and isinstance(cargo_details,list):
            cargo_details=cargo_details[0]
        if job_type==JobOrderType.CARTING_FCL.value:
            container_flag=ContainerFlag.FCL.value
            if constants.CCLS_CON_NUMBER in cargo_details:
                if cargo_details[constants.CCLS_CON_NUMBER]:
                    cargo_details[constants.CCLS_CRN_NUMBER]=cargo_details.pop(constants.CCLS_CON_NUMBER)
                else:
                    cargo_details[constants.CCLS_CRN_NUMBER]=crn_number
                cargo_details[constants.CCLS_CRN_DATE]=cargo_details.pop(constants.CCLS_CON_DATE)
            self.check_date_and_format_type(cargo_details,constants.CCLS_CRN_DATE)
        else:
            container_flag=ContainerFlag.LCL.value
            self.check_date_and_format_type(cargo_details,constants.CCLS_CON_DATE)
        if 'cha_Name' in cargo_details:
            cargo_details["cha_name"]=cargo_details["cha_Name"]
        # if "is_cargo_card_generated" not in cargo_details:
        cargo_details["is_cargo_card_generated"]='Y'
        if "reserve_flag" in cargo_details and cargo_details['reserve_flag'] is False:
            cargo_details["reserve_flag"]='Y'
        if "max_date_unloading" in cargo_details and cargo_details['max_date_unloading'] :
            if isinstance(cargo_details['max_date_unloading'],str):
                try:
                    cargo_details['max_date_unloading'] = int(cargo_details['max_date_unloading'])
                except Exception as e:
                    max_date_unloading = cargo_details['max_date_unloading'].replace('T',' ')
                    cargo_details['max_date_unloading'] = datetime.strptime(max_date_unloading, '%Y-%m-%d %H:%M:%S.%f%z')
            if isinstance(cargo_details['max_date_unloading'],datetime):
                cargo_details['max_date_unloading']=convert_ccls_date_to_timestamp(cargo_details['max_date_unloading'])
        self.update_shipping_bill_details(cargo_details)
        self.update_container(cargo_details)
        self.update_truck_details(cargo_details)

        cargo_details = self.update_carting_details_schema_for_serializer(cargo_details)
        self.update_params(cargo_details,job_type,container_flag)
        return cargo_details

    def update_stuffing_details(self,cargo_details,job_type):
        if job_type==JobOrderType.STUFFING_FCL.value:
            container_flag = ContainerFlag.FCL.value
        elif job_type==JobOrderType.STUFFING_LCL.value :
            container_flag = ContainerFlag.LCL.value
        else:
            container_flag = ContainerFlag.FCL.value
        if cargo_details and isinstance(cargo_details,list):
            cargo_details=cargo_details[0]
        if "stuffing_job_order" not in cargo_details or not cargo_details['stuffing_job_order']:
            cargo_details["stuffing_job_order"]='Y'
        self.update_shipping_bill_details(cargo_details)
        self.update_container(cargo_details)
        cargo_details = self.update_stuffing_details_schema_for_serializer(cargo_details)
        self.update_params(cargo_details,job_type,container_flag)
        return cargo_details

    def update_destuffing_details(self,cargo_details,job_type):
        if job_type==JobOrderType.DE_STUFFING_FCL.value:
            container_flag = ContainerFlag.FCL.value
        else:
            container_flag = ContainerFlag.LCL.value
        if cargo_details and isinstance(cargo_details,list):
            cargo_details=cargo_details[0]
        # if "destuffing_job_order" not in cargo_details:
            # cargo_details["destuffing_job_order"]=None
        self.check_date_and_format_type(cargo_details,"destuffing_plan_date")
        self.update_bill_details(cargo_details,container_flag)
        self.update_container(cargo_details)
        cargo_details = self.update_destuffing_details_schema_for_serializer(cargo_details)
        self.update_params(cargo_details,job_type,container_flag)
        return cargo_details

    def update_delivery_details(self,cargo_details,job_type):
        if job_type==JobOrderType.DELIVERY_FCL.value:
            container_flag = ContainerFlag.FCL.value
        elif job_type==JobOrderType.DELIVERY_LCL.value:
            container_flag = ContainerFlag.LCL.value
        else:
            container_flag = ContainerFlag.FCL.value
        if cargo_details and isinstance(cargo_details,list):
            cargo_details=cargo_details[0]
        self.check_date_and_format_type(cargo_details,constants.CCLS_GPM_VALIDATE_DATE)
        self.check_date_and_format_type(cargo_details,constants.CCLS_GPM_CREATED_DATE)
        self.update_bill_details(cargo_details,container_flag)
        self.update_truck_details(cargo_details)
        self.update_container(cargo_details)
        cargo_details = self.update_delivery_details_schema_for_serializer(cargo_details)
        self.update_params(cargo_details,job_type,container_flag)
        return cargo_details
    
    def check_date_and_format_type(self,cargo_details,date_key):
        if date_key in cargo_details and cargo_details[date_key] :
            if isinstance(cargo_details[date_key],str):
                try:
                    cargo_details[date_key] = int(cargo_details[date_key])
                except Exception as e:
                    max_date_unloading = cargo_details[date_key].replace('T',' ')
                    cargo_details[date_key] = datetime.strptime(max_date_unloading, '%Y-%m-%d %H:%M:%S.%f%z')
            if isinstance(cargo_details[date_key],datetime):
                cargo_details[date_key]=convert_ccls_date_to_timestamp(cargo_details[date_key])
        else:
            cargo_details[date_key]=int(time.time())*1000
