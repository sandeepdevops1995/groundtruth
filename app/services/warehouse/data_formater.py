import app.services.warehouse.constants as constants
from app.enums import ContainerFlag

class DataFormater(object):
    
    def build_carting_response_obj(self,job_order_details,container_flag):
        carting_job_obj = {'truck_details':job_order_details['truck_details'],"is_cargo_card_generated":job_order_details[constants.CCLS_IS_CARGO_CARD_GENERATED]}
        if container_flag==ContainerFlag.FCL.value:
            carting_job_obj.update({'crn_number' : job_order_details[constants.CCLS_CRN_NUMBER]})
        else:
            carting_job_obj.update({'cargo_carting_number' : job_order_details[constants.CCLS_CON_NUMBER]})
        key_list = {'bill_number_key':'shipping_bill','ccls_bill_number_key':constants.CCLS_SHIPPING_BILL_NUMBER,'ccls_bill_date_key':constants.CCLS_SHIPPING_BILL_DATE,'job_list_key_name':'shipping_bill_details_list'}
        result = self.build_response_obj(job_order_details,key_list,carting_job_obj)
        return result

    def build_stuffing_response_obj(self,job_order_details):
        stuffing_job_obj = {'crn_number' : job_order_details[constants.CCLS_CRN_NUMBER],'container_number' : job_order_details[constants.CCLS_CONTAINER_NUMBER],"stuffing_job_order":job_order_details['stuffing_job_order']}
        key_list = {'bill_number_key':'shipping_bill','ccls_bill_number_key':constants.CCLS_SHIPPING_BILL_NUMBER,'ccls_bill_date_key':constants.CCLS_SHIPPING_BILL_DATE,'job_list_key_name':'shipping_bill_details_list'}
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
        key_list = {'bill_number_key':bill_number_key,'ccls_bill_number_key':ccls_bill_number_key,'ccls_bill_date_key':constants.CCLS_BILL_DATE,'job_list_key_name':'bill_details_list'}
        result = self.build_response_obj(job_order_details,key_list,destuffing_job_obj)
        return result

    def build_delivery_response_obj(self,job_order_details,container_flag):
        delivery_job_obj = {'gpm_number' : job_order_details[constants.CCLS_GPM_NUMBER],'truck_details':job_order_details['truck_details']}
        key_list = {'bill_number_key':'bill_of_entry','ccls_bill_number_key':constants.CCLS_BILL_OF_ENTRY_NUMBER,'job_list_key_name':'bill_details_list'}
        if container_flag==ContainerFlag.LCL.value:
            key_list.update({'bill_number_key_one':'bill_of_lading','ccls_bill_number_key_one':constants.CCLS_BILL_OF_LADEN_NUMBER,'ccls_bill_date_key':constants.CCLS_BILL_DATE})
        result = self.build_response_obj(job_order_details,key_list,delivery_job_obj)
        return result
    
    def build_response_obj(self,job_order_details,key_list,job_obj):
        bill_details= job_order_details[key_list['job_list_key_name']]
        result = {"crn_number":None,"cargo_carting_number":None,"gpm_number":None,"container_number":None,'sline_code':job_order_details.get('shipping_liner_code',None)}
        result.update(job_obj)
        cargo_details = []
        total_package_count = 0
        for each_bill in bill_details:
             each_cargo_details = {"shipping_bill":None,"bill_of_entry":None,"bill_of_lading":None,'bill_date': each_bill[key_list['ccls_bill_date_key']]}
             each_cargo_details[key_list['bill_number_key']] = each_bill[key_list['ccls_bill_number_key']]
             if 'bill_number_key_one' in key_list:
                 each_cargo_details[key_list['bill_number_key_one']] = each_bill[key_list['ccls_bill_number_key_one']]
             each_cargo_details['cha_code'] = each_bill.get(constants.CCLS_CHA_CODE,None) if constants.CCLS_CHA_CODE in each_bill else job_order_details.get(constants.CCLS_CHA_CODE,None)
             each_cargo_details['commodity_details'] = []
             total_package_count+=int(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED])
             each_cargo_details['commodity_details'].append({'commodity_code':int(each_bill[constants.CCLS_COMMODITY_CODE]),'commodity_description':each_bill[constants.CCLS_COMMODITY_DESCRIPTION],'package_code':each_bill[constants.CCLS_PACKAGE_CODE],'package_count':int(each_bill[constants.CCLS_NO_OF_PACKAGES_DECLARED]),'package_weight':int(each_bill[constants.CCLS_PACKAGE_WEIGHT])})
             cargo_details.append(each_cargo_details)
        result['cargo_details'] = cargo_details
        result['total_package_count'] = total_package_count
        return result