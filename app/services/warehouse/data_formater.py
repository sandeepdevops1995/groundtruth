import app.services.warehouse.constants as constants
from app.enums import ContainerFlag

class DataFormater(object):
    def container_table_formater(self,job_details):
        container_details = {}
        container_details['container_number'] = job_details[constants.CCLS_CONTAINER_NUMBER] if constants.CCLS_CONTAINER_NUMBER in job_details else None
        container_details['container_type'] = job_details[constants.CCLS_CONTAINER_TYPE] if constants.CCLS_CONTAINER_TYPE in job_details else None
        container_details['container_size'] =  job_details[constants.CCLS_CONTAINER_SIZE] if constants.CCLS_CONTAINER_SIZE in job_details else None
        container_details['container_iso_code'] = job_details[constants.CCLS_CONTAINER_ISO_CODE] if constants.CCLS_CONTAINER_ISO_CODE in job_details else None
        return container_details
    

    def ctms_job_order_table_formater(self,tallysheet_data):
        tally_sheet_job_order_obj = {}
        tally_sheet_job_order_obj['equipment_id'] = tallysheet_data[constants.BACKEND_EQUIPMENT_ID] if constants.BACKEND_EQUIPMENT_ID in tallysheet_data else None
        tally_sheet_job_order_obj['ph_location'] = tallysheet_data[constants.BACKEND_PH_LOCATION] if constants.BACKEND_PH_LOCATION in tallysheet_data else None
        tally_sheet_job_order_obj['job_start_time'] = tallysheet_data[constants.BACKEND_JOB_START_TIME] if constants.BACKEND_JOB_START_TIME in tallysheet_data else None
        tally_sheet_job_order_obj['job_end_time'] = tallysheet_data[constants.BACKEND_JOB_END_TIME] if constants.BACKEND_JOB_END_TIME in tallysheet_data else None
        tally_sheet_job_order_obj['total_package_count'] = tallysheet_data[constants.BACKEND_TOTAL_NO_OF_PACKAGES_JOB_DONE] if constants.BACKEND_TOTAL_NO_OF_PACKAGES_JOB_DONE in tallysheet_data else None
        tally_sheet_job_order_obj['total_no_of_packages_damaged'] = tallysheet_data[constants.BACKEND_TOTAL_NO_OF_PACKAGES_DAMAGED] if constants.BACKEND_TOTAL_NO_OF_PACKAGES_DAMAGED in tallysheet_data else None
        tally_sheet_job_order_obj['total_no_area'] = tallysheet_data[constants.BACKEND_TOTAL_NO_AREA] if constants.BACKEND_TOTAL_NO_AREA in tallysheet_data else None
        tally_sheet_job_order_obj['max_date_unloading'] = tallysheet_data[constants.BACKEND_MAX_DATE_UNLOADING] if constants.BACKEND_MAX_DATE_UNLOADING in tallysheet_data else None
        tally_sheet_job_order_obj['total_no_of_packages_excess'] = tallysheet_data[constants.BACKEND_TOTAL_NO_OF_PACKAGES_EXCESS] if constants.BACKEND_TOTAL_NO_OF_PACKAGES_EXCESS in tallysheet_data else None
        tally_sheet_job_order_obj['total_no_of_packages_short'] = tallysheet_data[constants.BACKEND_TOTAL_NO_OF_PACKAGES_SHORT] if constants.BACKEND_TOTAL_NO_OF_PACKAGES_SHORT in tallysheet_data else None
        tally_sheet_job_order_obj['gate_number'] = tallysheet_data[constants.BACKEND_GATE_NUMBER] if constants.BACKEND_GATE_NUMBER in tallysheet_data else None
        tally_sheet_job_order_obj['warehouse_name'] = tallysheet_data[constants.BACKEND_WAREHOUSE_NAME] if constants.BACKEND_WAREHOUSE_NAME in tallysheet_data else None
        tally_sheet_job_order_obj['job_start_time'] = tallysheet_data[constants.BACKEND_START_TIME] if constants.BACKEND_START_TIME in tallysheet_data else None
        tally_sheet_job_order_obj['job_end_time'] = tallysheet_data[constants.BACKEND_END_TIME] if constants.BACKEND_END_TIME in tallysheet_data else None
        tally_sheet_job_order_obj['created_on_epoch'] = int(tallysheet_data['created_on_epoch']) if 'created_on_epoch' in tallysheet_data else None
        return tally_sheet_job_order_obj
    
    def ctms_cargo_details_table_formater(self,tallysheet_bill_details):
        tallysheet_bill_detail_obj = {}
        tallysheet_bill_detail_obj['package_weight'] = tallysheet_bill_details[constants.BACKEND_PACKAGE_WEIGHT] if constants.BACKEND_PACKAGE_WEIGHT in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['damaged_packages_weight'] = tallysheet_bill_details[constants.BACKEND_DAMAGED_PACKAGES_WEIGHT] if constants.BACKEND_DAMAGED_PACKAGES_WEIGHT in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['package_count'] = tallysheet_bill_details[constants.BACKEND_PACKAGE_COUNT] if constants.BACKEND_PACKAGE_COUNT in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['no_of_packages_damaged'] = tallysheet_bill_details[constants.BACKEND_NO_OF_PACKAGES_DAMAGED] if constants.BACKEND_NO_OF_PACKAGES_DAMAGED in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['cha_code'] = tallysheet_bill_details[constants.BACKEND_CHA_CODE] if constants.BACKEND_CHA_CODE in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['full_or_part_destuff'] = tallysheet_bill_details[constants.BACKEND_FULL_OR_PART_DESTUFF] if constants.BACKEND_FULL_OR_PART_DESTUFF in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['area'] = tallysheet_bill_details[constants.BACKEND_AREA] if constants.BACKEND_AREA in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['area_damaged'] = tallysheet_bill_details[constants.BACKEND_AREA_DAMAGED] if constants.BACKEND_AREA_DAMAGED in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['grid_number'] = tallysheet_bill_details[constants.BACKEND_GRID_NUMBER] if constants.BACKEND_GRID_NUMBER in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['grid_locations'] = tallysheet_bill_details[constants.BACKEND_GRID_LOCATIONS] if constants.BACKEND_GRID_LOCATIONS in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['truck_number'] = tallysheet_bill_details[constants.BACKEND_TRUCK_NUMBER] if constants.BACKEND_TRUCK_NUMBER in tallysheet_bill_details else None
        # tallysheet_bill_detail_obj['container_number'] = tallysheet_bill_details[constants.BACKEND_CONTAINER_NUMBER] if constants.BACKEND_CONTAINER_NUMBER in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['start_time'] = tallysheet_bill_details[constants.BACKEND_START_TIME] if constants.BACKEND_START_TIME in tallysheet_bill_details else None
        tallysheet_bill_detail_obj['end_time'] = tallysheet_bill_details[constants.BACKEND_END_TIME] if constants.BACKEND_END_TIME in tallysheet_bill_details else None
        return tallysheet_bill_detail_obj

    def ccls_job_order_table_formater(self,job_details):
        job_order_obj = {}
        job_order_obj['con_date'] = job_details[constants.CCLS_CON_DATE] if constants.CCLS_CON_DATE in job_details else None
        job_order_obj['crn_date'] = job_details[constants.CCLS_CRN_DATE] if constants.CCLS_CRN_DATE in job_details else None
        job_order_obj['shipping_liner_code'] = job_details[constants.CCLS_SHIPPING_LINER_CODE] if constants.CCLS_SHIPPING_LINER_CODE in job_details else None
        job_order_obj['party_code'] = job_details[constants.CCLS_PARTY_CODE] if constants.CCLS_PARTY_CODE in job_details else None
        job_order_obj['cha_code'] = job_details[constants.CCLS_CHA_CODE] if constants.CCLS_CHA_CODE in job_details else None
        job_order_obj['gw_port_code'] = job_details[constants.CCLS_GW_PORT_CODE] if constants.CCLS_GW_PORT_CODE in job_details else None
        job_details['container_location_code'] = job_details[constants.CCLS_CONTAINER_LOCATION_CODE] if constants.CCLS_CONTAINER_LOCATION_CODE in job_details else None
        job_details['container_life'] = job_details[constants.CCLS_CONTAINER_LIFE] if constants.CCLS_CONTAINER_LIFE in job_details else None
        job_order_obj['gross_weight'] = job_details[constants.CCLS_GROSS_WEIGHT] if constants.CCLS_GROSS_WEIGHT in job_details else None
        job_order_obj['gpm_number'] = job_details[constants.CCLS_GPM_NUMBER] if constants.CCLS_GPM_NUMBER in job_details else None
        job_order_obj['gpm_created_date'] = job_details[constants.CCLS_GPM_CREATED_DATE] if constants.CCLS_GPM_CREATED_DATE in job_details else None
        job_order_obj['carting_order_number'] = job_details[constants.CCLS_CON_NUMBER] if constants.CCLS_CON_NUMBER in job_details else None
        job_order_obj['crn_number'] = job_details[constants.CCLS_CRN_NUMBER] if constants.CCLS_CRN_NUMBER in job_details else None
        job_order_obj['cargo_weight_in_crn'] = job_details[constants.CCLS_CARGO_WEIGHT_IN_CRN] if constants.CCLS_CARGO_WEIGHT_IN_CRN in job_details else None
        job_order_obj['weight_remaining'] = job_details[constants.CCLS_WEIGHT_REMAINING] if constants.CCLS_WEIGHT_REMAINING in job_details else None
        job_order_obj['stuffing_job_order'] = job_details[constants.CCLS_STUFFING_JOB_ORDER] if constants.CCLS_STUFFING_JOB_ORDER in job_details else None
        job_order_obj['destuffing_job_order'] = job_details[constants.CCLS_DESTUFFING_JOB_ORDER] if constants.CCLS_DESTUFFING_JOB_ORDER in job_details else None
        job_order_obj['private_or_concor_labour_flag'] = job_details[constants.CCLS_PRIVATE_OR_CONCOR_LABOUR_FLAG] if constants.CCLS_PRIVATE_OR_CONCOR_LABOUR_FLAG in job_details else None
        job_order_obj['handling_code'] = job_details[constants.CCLS_HANDLING_CODE] if constants.CCLS_HANDLING_CODE in job_details else None
        job_order_obj['icd_location_code'] = job_details[constants.CCLS_ICD_LOCATION_CODE] if constants.CCLS_ICD_LOCATION_CODE in job_details else None
        job_order_obj['is_cargo_card_generated'] = job_details[constants.CCLS_IS_CARGO_CARD_GENERATED] if constants.CCLS_IS_CARGO_CARD_GENERATED in job_details else None
        job_order_obj['reserve_flag'] = job_details[constants.CCLS_REVERSE_FLAG] if constants.CCLS_REVERSE_FLAG in job_details else None
        job_order_obj['job_type'] = job_details[constants.BACKEND_JOB_TYPE] if constants.BACKEND_JOB_TYPE in job_details else None
        job_order_obj['fcl_or_lcl'] = job_details[constants.BACKEND_CONTAINER_FLAG] if constants.BACKEND_CONTAINER_FLAG in job_details else None
        return job_order_obj
    
    def ccls_cargo_details_table_formater(self,bill_details):
        bill_detail_obj = {}
        bill_detail_obj['commodity_id'] = bill_details[constants.CCLS_COMMODITY_ID] if constants.CCLS_COMMODITY_ID in bill_details else None
        bill_detail_obj['shipping_bill'] = bill_details[constants.CCLS_SHIPPING_BILL_NUMBER] if constants.CCLS_SHIPPING_BILL_NUMBER in bill_details else None
        bill_detail_obj['bill_of_entry'] = bill_details[constants.CCLS_BILL_OF_ENTRY_NUMBER] if constants.CCLS_BILL_OF_ENTRY_NUMBER in bill_details else None
        bill_detail_obj['bill_of_lading'] = bill_details[constants.CCLS_BILL_OF_LADEN_NUMBER] if constants.CCLS_BILL_OF_LADEN_NUMBER in bill_details else None
        bill_detail_obj['bill_date'] = bill_details[constants.CCLS_BILL_DATE] if constants.CCLS_BILL_DATE in bill_details else bill_details[constants.CCLS_SHIPPING_BILL_DATE] if constants.CCLS_SHIPPING_BILL_DATE in bill_details else None
        bill_detail_obj['importer_code'] = bill_details[constants.CCLS_IMPORTER_CODE] if constants.CCLS_IMPORTER_CODE in bill_details else None
        bill_detail_obj['importer_name'] = bill_details[constants.CCLS_IMPORTER_NAME] if constants.CCLS_IMPORTER_NAME in bill_details else None
        bill_detail_obj['package_code'] = bill_details[constants.CCLS_PACKAGE_CODE] if constants.CCLS_PACKAGE_CODE in bill_details else None
        bill_detail_obj['no_of_packages_declared'] = bill_details[constants.CCLS_NO_OF_PACKAGES_DECLARED] if constants.CCLS_NO_OF_PACKAGES_DECLARED in bill_details else None
        bill_detail_obj['package_weight'] = bill_details[constants.CCLS_PACKAGE_WEIGHT] if constants.CCLS_PACKAGE_WEIGHT in bill_details else None
        bill_detail_obj['job_order_id'] = bill_details[constants.CCLS_JOB_ORDER_ID] if constants.CCLS_JOB_ORDER_ID in bill_details else None
        bill_detail_obj['cha_code'] = bill_details[constants.CCLS_CHA_CODE] if constants.CCLS_CHA_CODE in bill_details else None
        return bill_detail_obj
    
    def build_carting_response_obj(self,job_order_details,container_flag):
        print("job_order_details----------------",job_order_details)
        if container_flag==ContainerFlag.FCL.value:
            carting_job_obj = {'crn_number' : job_order_details[constants.CCLS_CRN_NUMBER],'truck_details':job_order_details['truck_details']}
        else:
            carting_job_obj = {'cargo_carting_number' : job_order_details[constants.CCLS_CON_NUMBER],'truck_details':job_order_details['truck_details']}
        key_list = {'bill_number_key':'shipping_bill','ccls_bill_number_key':constants.CCLS_SHIPPING_BILL_NUMBER,'job_list_key_name':'shipping_bill_details_list'}
        result = self.build_response_obj(job_order_details,key_list,carting_job_obj)
        return result

    def build_stuffing_response_obj(self,job_order_details):
        stuffing_job_obj = {'crn_number' : job_order_details[constants.CCLS_CRN_NUMBER],'container_number' : job_order_details[constants.CCLS_CONTAINER_NUMBER],"stuffing_job_order":job_order_details['stuffing_job_order']}
        key_list = {'bill_number_key':'shipping_bill','ccls_bill_number_key':constants.CCLS_SHIPPING_BILL_NUMBER,'job_list_key_name':'shipping_bill_details_list'}
        result = self.build_response_obj(job_order_details,key_list,stuffing_job_obj)
        return result

    def build_destuffing_response_obj(self,job_order_details,container_flag):
        if container_flag==ContainerFlag.FCL.value:
            bill_number_key = 'bill_of_entry'
            ccls_bill_number_key =  constants.CCLS_BILL_OF_ENTRY_NUMBER
        else:
            bill_number_key = 'bill_of_lading'
            ccls_bill_number_key =  constants.CCLS_BILL_OF_LADEN_NUMBER
        destuffing_job_obj = {'container_number' : job_order_details[constants.CCLS_CONTAINER_NUMBER],'destuffing_job_order':job_order_details['destuffing_job_order']}
        key_list = {'bill_number_key':bill_number_key,'ccls_bill_number_key':ccls_bill_number_key,'job_list_key_name':'bill_details_list'}
        result = self.build_response_obj(job_order_details,key_list,destuffing_job_obj)
        return result

    def build_delivery_response_obj(self,job_order_details,container_flag):
        delivery_job_obj = {'gpm_number' : job_order_details[constants.CCLS_GPM_NUMBER],'truck_details':job_order_details['truck_details']}
        key_list = {'bill_number_key':'bill_of_entry','ccls_bill_number_key':constants.CCLS_BILL_OF_ENTRY_NUMBER,'job_list_key_name':'bill_details_list'}
        if container_flag==ContainerFlag.LCL.value:
            key_list.update({'bill_number_key_one':'bill_of_entry','ccls_bill_number_key_one':constants.CCLS_BILL_OF_LADEN_NUMBER})
        result = self.build_response_obj(job_order_details,key_list,delivery_job_obj)
        return result
    
    def build_response_obj(self,job_order_details,key_list,job_obj):
        bill_details= job_order_details[key_list['job_list_key_name']]
        result = {"crn_number":None,"cargo_carting_number":None,"gpm_number":None,"container_number":None,'sline_code':job_order_details.get('sline_code','AA1233')}
        result.update(job_obj)
        cargo_details = []
        total_package_count = 0
        for each_bill in bill_details:
             each_cargo_details = {"shipping_bill":None,"bill_of_entry":None,"bill_of_lading":None}
             each_cargo_details[key_list['bill_number_key']] = each_bill[key_list['ccls_bill_number_key']]
             if 'bill_number_key_one' in key_list:
                 each_cargo_details[key_list['bill_number_key_one']] = each_bill[key_list['ccls_bill_number_key_one']]
            #  each_cargo_details['sline_code'] = job_order_details.get(constants.CCLS_SHIPPING_LINER_CODE,None)
             each_cargo_details['cha_code'] = job_order_details.get(constants.CCLS_CHA_CODE,None)
             each_cargo_details['commodity_details'] = []
             total_package_count+=int(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED])
             each_cargo_details['commodity_details'].append({'commodity_code':int(each_bill[constants.CCLS_COMMODITY_CODE]),'commodity_description':each_bill[constants.CCLS_COMMODITY_DESCRIPTION],'package_code':each_bill[constants.CCLS_PACKAGE_CODE],'package_count':int(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED]),'package_weight':int(each_bill[constants.CCLS_PACKAGE_WEIGHT])})
             cargo_details.append(each_cargo_details)
        result['cargo_details'] = cargo_details
        result['total_package_count'] = total_package_count
        return result